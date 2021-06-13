# CARE-2021

## Saliency Maps

- Code for generating  saliency maps is present in `saliency_maps.ipynb` notebook.
- There is a pretrained model in the repo `stage-3-fine-tuned-res50.pkl`. It is being loaded in notebook, use it for inference tasks or CAM generation
- Final results are stored in final folder (exported directly from toloka)
  -  Aggregation based on final results are performed in Final Aggregation.ipynb

## Quality Control

qc.py includes functions for running majority voting (fixed_annotations, free_text fubcs) and crowdtruth metrics (helper func) on Toloka labeling output. Due to high variability in json outputs (free text vs fine grained vs coarse grained) different annotation extraction parts are commented out within these functions.

### Library dependencies
- pytorch
- fastai
- slugify
- stringcase
- matplotlib
- scikit-image
- tqdm
- pandas
- deep_translator
- CrowdTruth
