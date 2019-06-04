# ****************** Goal *******************
Getting structural MRIs that are ready to be put on a server, or to be shared.
This requires a standardized format (nifti), naming (we will follow BIDS) and removal of identity in the header and on the scan itself (face).


# ****************** A bit of background *******************
https://open-brain-consent.readthedocs.io/en/stable/anon_tools.html
download and compile: https://biabl.com/getting-started

discussion of issues: link.springer.com/content/pdf/10.1007%2F978-3-642-22348-8_26.pdf


# ****************** Tools to choose from *******************

1. Convert dicom to nifti:
dcm2niix; https://github.com/rordenlab/dcm2niix

2. Taking out personal information in header:
Through dcm2niix
https://www.nitrc.org/projects/de-identification
https://pydicom.github.io/deid/

3. Defacing:
pydeface: https://github.com/poldrack/python
mri_deface: https://surfer.nmr.mgh.harvard.edu/fswiki/mri_deface
BIDSonym: https://github.com/PeerHerholz/BIDSonym
-> I wanted to try BIDSonym but I would need to learn how to use Docker, etc…, so I went straight to pydeface


# ****************** Steps to completion *******************

# * Updates and installs:
In terminal:
conda update conda
conda update anaconda
conda install -c conda-forge dcm2niix

In terminal:
Fsl (to check if already there); if not: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation/MacOsX
(after having activated the environment that contains python 2.7; e.g. source activate dev27 if you have it set up in anaconda)
pip install nibabel
conda install nipype

then:
git clone https://github.com/poldracklab/pydeface.git
cd pydeface
python setup.py install

# * Examples of commands:
In terminal:
dcm2niix -b y -f sub-XX_T1w -o /Volumes/CBradleyQBI/TMS-EEG-Visual/data/sourcedata/XXX_participant /Volumes/CBradleyQBI/MRIs/XXX_participant/MPRAGE

In terminal:
pydeface /Volumes/CBradleyQBI/TMS-EEG-Visual/data/sub-XX/anat/sub-XX_T1w.nii --outfile /Volumes/CBradleyQBI/TMS-EEG-Visual/data/sub-XX/anat/sub-XX_T1w.nii --force

# -----> Full script: AnatomicalMRI_DICOM2Nifti_Deface
