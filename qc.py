import itertools
import math
import unicodedata

import crowdtruth
from crowdtruth.configuration import DefaultConfig
import json

import json
import pandas as pd
from deep_translator import GoogleTranslator


def fixed_annotations(df, annotations_dict):
    for idx, row in df.iterrows():
        jsns = row['OUTPUT:path']
        img = row['INPUT:image_left']
        if jsns and str(jsns).lower() != 'nan':
            jsns = jsns.replace('},{', '}@@{').replace('\,', ',').split('@@')
            print(jsns)
            for jsn in jsns:
                print(jsn)
                annn = json.loads(jsn)
                try:
                    for ann in annn['label'].split(' & '):
                        print(ann)
                        # ann = unicodedata.normalize('NFD', ann['label']).lower()
                        # ann = GoogleTranslator(source='ru', target='en').translate(ann)
                        if img in annotations_dict.keys():
                            if ann in annotations_dict[img].keys():
                                annotations_dict[img][ann] += 1
                            else:
                                annotations_dict[img][ann] = 1
                        else:
                            annotations_dict[img] = {}
                            annotations_dict[img][ann] = 1
                except Exception as e:
                    print(e)
                    pass

    return annotations_dict


def free_text(df, annotations_dict, col):
    # for idx, row in df.iterrows():
    #     jsns = row['OUTPUT:result']
    #     img = row['INPUT:image_left']
    #     if jsns and str(jsns).lower() != 'nan':
    #         for ann in json.loads(jsns):
    #             try:
    #                 ann = ann['annotation']
    #                 ann = ann.replace('\\', '').replace('"', '').lower()
    #                 while ann[0] == ' ':
    #                     ann = ann[1:]
    #                 while ann[-1] == ' ':
    #                     ann = ann[:-1]
    #
    #                 # ann = unicodedata.normalize('NFD', ann).lower()
    #                 try:
    #                     ann = GoogleTranslator(source='ru', target='en').translate(ann)
    #                 except:
    #                     pass
    #                 print(ann)
    #                 df.loc[idx, col] = ann
    #                 if img in annotations_dict.keys():
    #                     if ann in annotations_dict[img].keys():
    #                         annotations_dict[img][ann] += 1
    #                     else:
    #                         annotations_dict[img][ann] = 1
    #                 else:
    #                     annotations_dict[img] = {}
    #                     annotations_dict[img][ann] = 1
    #             except Exception as e:
    #                 print(e)
    #                 pass

    for idx, row in df.iterrows():
        jsns = row['OUTPUT:result']
        img = row['INPUT:image_left']
        if jsns and str(jsns).lower() != 'nan':
            jsn = json.loads(jsns)
            print(jsn)
            for a, bl in jsn.items():
                try:
                    ann = unicodedata.normalize('NFD', a).lower()
                    # ann = GoogleTranslator(source='ru', target='en').translate(ann)
                    if img in annotations_dict.keys():
                        if ann in annotations_dict[img].keys():
                            annotations_dict[img][ann] += 1
                        else:
                            annotations_dict[img][ann] = 1
                    else:
                        annotations_dict[img] = {}
                        annotations_dict[img][ann] = 1
                except Exception as e:
                    pass

    return annotations_dict, df


class TestConfig(DefaultConfig):
    inputColumns = ["INPUT:image_right"]
    outputColumns = ["OUTPUT:result"]
    # change this based on inpput tsv
    customPlatformColumns = ["ASSIGNMENT:assignment_id", "ASSIGNMENT:task_suite_id", "ASSIGNMENT:worker_id",
                             "ASSIGNMENT:started", "ASSIGNMENT:submitted"]
    annotation_separator = ','

    # processing of a closed task
    open_ended_task = False
    # annotation_vector = ['beak', 'eye', 'head', 'wing', 'torso', 'pupil', 'throat', 'flanks', 'primaries', 'not head',
    #                      'nape', 'ear coverts', 'belly', 'chest', 'skull', 'body', 'wings', '1']


def process(x):
    if x is not None:
        x = list(map(lambda y: y.lower(), x))
    return x


def process2(x):
    if x is not None:
        x = map(lambda y: y.strip(), x)
    return x


def custom_translate(x):
    while x[0] == ' ':
        x = x[1:]
    while x[-1] == ' ':
        x = x[:-1]
    try:
        x = GoogleTranslator(source='ru', target='en').translate(x)
    except Exception as e:
        print(e)
    return x


def helper(tsv_file, tp):
    csv_table = pd.read_table(tsv_file, sep='\t')
    csv_table = csv_table.drop(columns=['INPUT:image_left', 'HINT:text',
                                        'HINT:default_language'])
    csv_table = csv_table.rename(columns={"OUTPUT:path": "OUTPUT:result"})
    csv_table = csv_table[csv_table['INPUT:image_right'].notna()]
    df_new = None

    # 1st version tsv - free text
    # some pilots have 'annotation' instead of 'label'!
    if tp == 1:
        print(str(csv_table['OUTPUT:result'][0]).replace('},{', '}@@{').split('@@'))
        csv_table['OUTPUT:result'] = csv_table['OUTPUT:result'].apply(
            lambda x: [json.loads(x)['annotation'] if 'annotation' in json.loads(x) else None for x in
                       str(x).replace('},{', '}@@{').replace('[', ''). replace(']', '').split('@@')])
        csv_table['OUTPUT:result'] = csv_table['OUTPUT:result'].apply(lambda x: ','.join([custom_translate(z).lower() for z in x]) if x[0] else pd.NaT)
        csv_table = csv_table.dropna(subset=['OUTPUT:result'])
        print(csv_table['OUTPUT:result'])

        df_new = csv_table

    if tp == 3:
        print(csv_table['OUTPUT:result'])
        csv_table['OUTPUT:result'] = csv_table['OUTPUT:result'].apply(
            lambda x: x.replace('\\', '').replace('"', '').lower().split(', ') if str(x).lower() != 'nan' else None)
        csv_table['OUTPUT:result'] = csv_table['OUTPUT:result'].apply(lambda x: ','.join([custom_translate(y) for y in x]).replace(', ', ',') if x else None)

        df_new = csv_table
        print(csv_table['OUTPUT:result'])

    # 3rd version tsv - fixed text
    if tp == 2:
        print(csv_table['OUTPUT:result'][0])
        csv_table['OUTPUT:result'] = csv_table['OUTPUT:result'].apply(lambda x: ','.join(list(json.loads(x).keys())).lower())
        print(csv_table['OUTPUT:result'])

        df_new = csv_table

    if tp == 0:
        print(str(csv_table['OUTPUT:result'][0]).replace('},{', '}@@{').replace('\\', '').split('@@'))
        csv_table['OUTPUT:result'] = csv_table['OUTPUT:result'].apply(
            lambda x: [json.loads(x)['label'].split(' & ') if 'label' in json.loads(x) else pd.NaT for x in
                       str(x).replace('},{', '}@@{').replace('[', '').replace('\\', '').replace(']', '').split('@@')])
        csv_table = csv_table.dropna(subset=['OUTPUT:result'])
        csv_table['OUTPUT:result'] = csv_table['OUTPUT:result'].apply(lambda x: ','.join(list(itertools.chain(*x))))
        print(csv_table['OUTPUT:result'])

        df_new = csv_table

    df_new['ASSIGNMENT:started'] = pd.to_datetime(csv_table['ASSIGNMENT:started'])
    df_new['ASSIGNMENT:submitted'] = pd.to_datetime(csv_table['ASSIGNMENT:submitted'])

    df_new.to_csv('v1.csv', index=False)
    print(df_new.columns)

    data, config = crowdtruth.load(
        file="v1.csv",
        config=TestConfig()
    )

    # data['judgments']['output.OUTPUT:result'] = data['judgments']['output.OUTPUT:result'].apply(lambda x: process2(x))
    print(type(data))
    print(data['judgments'])

    results = crowdtruth.run(data, config)
    print(results["units"].head())
    print(results["units"]["unit_annotation_score"].head())
    return results


def mv(f, tp):
    df = pd.read_table(f'./final/{f}.tsv', error_bad_lines=False)
    try:
        col = 'OUTPUT:path'
        df = df[['OUTPUT:path', 'INPUT:image_left']]
    except:
        col = 'OUTPUT:result'
        df = df[['OUTPUT:result', 'INPUT:image_left']]

    annotations_dict = {}

    if tp == 'fixed':
        annotations_dict, ann_df = fixed_annotations(df, annotations_dict)
    elif tp == 'free':
        annotations_dict, ann_df = free_text(df, annotations_dict, col)

    print(annotations_dict)
    with open(f'./final/mv_{f}.json', 'w') as outfile:
        json.dump(annotations_dict, outfile)


def ct(f, tp):
    res = helper(f'./pilots/{f}.tsv', tp)
    res["workers"].sort_values(by=["wqs"], ascending=False).to_csv(f'./pilots/wq_res_{f}.csv')
    res["units"]["unit_annotation_score"].to_csv(f'./pilots/res_{f}.csv')


if __name__ == '__main__':
    for f, tp in [('bb_group_003', 0), ('bb_grouped_02', 0), ('bb_text_003', 1),
                  ('pred_coarse_003', 2), ('pred_fine_003', 2), ('pred_text_003', 3)]:
        print(f)
        ct(f, tp)

    for f, tp in [('final_result1', 'free'), ('final_result2', 'free')]:
        mv(f, tp)
