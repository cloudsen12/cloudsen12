import maskay

# Donwload S2 an create a TenSorSat object
productid = "S2A_MSIL1C_20190212T142031_N0207_R010_T19FDF_20190212T191443"
#s2idpath = maskay.download.s2.SAFE(productid, "/content/", quiet=False)
s2idpath = "/home/csaybar/S2A_MSIL1C_20190212T142031_N0207_R010_T19FDF_20190212T191443.SAFE"
S2files = maskay.utils.MaskayDict(
    path=s2idpath,
    pattern="\.jp2$",
    full_names=True,
    recursive=True,
    sensor="Sentinel-2"
)
bands = S2files[[7, 3, 2, 1]]
tensor = maskay.TensorSat(**bands.to_dict(), cache=True, align=True)

# Make a prediction
#model = maskay.library.UnetMobV2()
#model = maskay.library.KappaModelUNetL1C()
#model = maskay.library.DynamicWorld()
model = maskay.library.CDFCNNrgbi()
predictor = maskay.Predictor(
    cropsize = 512,
    overlap = 32,
    device = "cpu",
    batchsize = 1,
    quiet = False,
    order = "BHWC"
)
result = predictor.predict(model, tensor)
result.shape
predictor.result.rio.to_raster("/home/csaybar/outensor2.tif")
 
import matplotlib.pyplot as plt
import numpy as np

xxx = predictor.result.to_numpy()[0:3]
xxx = predictor.result[0:3]
rtoplot = np.moveaxis(xxx, 0, -1)
plt.imshow(rtoplot/10000)
plt.show()
 

import timeit

aa = time.time()
#a = np.zeros((1, 9, 512, 512))*1.
test = np.ones((128, 128, 128))
np.sum(a) == 0
time.time() - aa
