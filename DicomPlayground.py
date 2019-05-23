#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def downsizeDicom(imgStack):
    import os
    import pydicom
    from pydicom.data import get_testdata_files
    for img in imgStack:
        # FIXME: add a full-sized MR image in the testing data
#         print("./dicom_folder/"+img)
#         filename = get_testdata_files(img)
#         print(filename)
        # local directory name
        ds = pydicom.dcmread("./dicom_folder/"+img)
#         print(ds);

        # get the pixel information into a numpy array
        data = ds.pixel_array
        print('The image has {} x {} voxels'.format(data.shape[0],
                                                    data.shape[1]))
        data_downsampling = data[::8, ::8]
        print('The downsampled image has {} x {} voxels'.format(
            data_downsampling.shape[0], data_downsampling.shape[1]))

        # copy the data back to the original data set
        ds.PixelData = data_downsampling.tobytes()
        # update the information regarding the shape of the data array
        ds.Rows, ds.Columns = data_downsampling.shape

        # print the image information given in the dataset
        print('The information of the data set after downsampling: \n')
        print(ds)
        ds.save_as("./dicom_folder/new_"+img)
        


# In[1]:


def flipHorizontalDicom(imgStack):
    import os
    import pydicom
    from pydicom.data import get_testdata_files
    for img in imgStack:
        # FIXME: add a full-sized MR image in the testing data
#         print("./dicom_folder/"+img)
#         filename = get_testdata_files(img)
#         print(filename)
        ds = pydicom.dcmread("./dicom_folder/"+img)
#         print(ds);

        # get the pixel information into a numpy array
        data = ds.pixel_array
        print(data)
        data = np.fliplr(data)
        print(data)
        ds.PixelData = data.tobytes()
        
        ds.save_as("./dicom_folder/new_"+img)


# In[5]:


def flipVerticalDicom(imgStack):
    import os
    import pydicom
    from pydicom.data import get_testdata_files
    for img in imgStack:
        # FIXME: add a full-sized MR image in the testing data
#         print("./dicom_folder/"+img)
#         filename = get_testdata_files(img)
#         print(filename)
        ds = pydicom.dcmread("./dicom_folder/"+img)
#         print(ds);

        # get the pixel information into a numpy array
        data = ds.pixel_array
        print(data)
        data = np.flipud(data)
        print(data)
        ds.PixelData = data.tobytes()
        
        ds.save_as("./dicom_folder/new_"+img)


# In[12]:


def rotateRandomDicom(imgStack):
    import os
    import pydicom
    import random
    from pydicom.data import get_testdata_files
    for img in imgStack:
        # FIXME: add a full-sized MR image in the testing data
#         print("./dicom_folder/"+img)
#         filename = get_testdata_files(img)
#         print(filename)
        ds = pydicom.dcmread("./dicom_folder/"+img)
#         print(ds);

        # get the pixel information into a numpy array
        data = ds.pixel_array
        print(data)
        data = np.rot90(data, random.randrange(0,3))
        print(data)
        ds.PixelData = data.tobytes()
        
        ds.save_as("./dicom_folder/new_"+img)


# In[13]:


# get dicom stack as a numpy array
from os import listdir
from os.path import isfile, join
mypath = "" # path to your working directory
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)
import numpy as np
a = np.array( onlyfiles )
print(a)
# call function
# downsizeDicom(a);
# flipHorizontalDicom(a);
# flipVerticalDicom(a);
rotateRandomDicom(a);


# In[ ]:


def save_as_dicom_file(data, num):
   import SimpleITK as sitk
   import time
   import os
   filtered_image = sitk.GetImageFromArray(data)
   writer = sitk.ImageFileWriter()
   # Use the study/seriers/frame of reference information given in the meta-data
   # dictionary and not the automatically generated information from the file IO
   # writer.KeepOriginalImageUIDOn()
   modification_time = time.strftime("%H%M%S")
   modification_date = time.strftime("%Y%m%d")
   print(filtered_image.GetDepth())
   for i in range(filtered_image.GetDepth()):
       image_slice = filtered_image[:,:,i]
       image_slice.SetMetaData("0008|0031", modification_time)
       image_slice.SetMetaData("0008|0021", modification_date)
       image_slice.SetMetaData("0008|0008", "DERIVED\SECONDARY")
       # Each of the UID components is a number (cannot start with zero) and separated by a '.'
       # We create a unique series ID using the date and time.
       image_slice.SetMetaData("0020|000e", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time)
       # Write to the output directory and add the extension dcm if not there, to force writing is in DICOM format.
       file_path = os.path.join('../mri_flip_h/new/',str(num))
       if not os.path.exists(file_path):
           os.mkdir(file_path)
       writer.SetFileName(os.path.join(file_path, str(i) + '.dcm'))
       writer.Execute(image_slice)


# In[ ]:




