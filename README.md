# CARE-2021

## Saliency Maps

- `saliency_maps.ipynb` contains code for generating  saliency maps
- `stage-3-fine-tuned-res50.pkl` is the pretrained model. It is loaded in `saliency_maps.ipynb` notebook, use it for inference tasks or CAM generation

## Quality Control

- `qc.py` includes functions for running majority voting (fixed_annotations, free_text fubcs) and crowdtruth metrics (helper func) on Toloka labeling output. Due to high variability in json outputs (free text vs fine grained vs coarse grained) different annotation extraction parts are commented out within these functions.

## Phase 2

- `phase2_analysis` folder contains post-processed outcomes of phase 2 using CrowdTruth
- `Phase2.ipynb` contains graph generation based upon the post-processed data

## Phase 3

-  `final` folder contains phase 3 checkbox outcomes (exported directly from toloka): 2 files for two completed pools
-  `Final Aggregation.ipynb` contains aggregation based on final results 


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
