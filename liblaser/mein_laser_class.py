import numpy as np
from scipy.interpolate import interp1d
import pandas as pd

from liblaser.perfilador import *

import cv2
import pdb





class LaserAnalyzer:
    def __init__(self,image, pixel_size,units,background_fraction,crop=True):
        self.LaserData=LaserData(image, pixel_size,units,background_fraction,crop)
        self.Semiminor=Semiminor(self.LaserData)
        self.Semimajor=Semimajor(self.LaserData)



    def calibrate_LaserData_backgraund_noise(self):
        correla=[]
        valor=[]
        for i in np.linspace(0.035,0.50,100):
            prueba=LaserData(self.LaserData.image1, self.LaserData.pixel_size, units='μm',background_fraction=i)
            zx=prueba.zx
            s=prueba.sx
            a = prueba.a
            if np.any(zx > 0): 
                zx=100*zx/max(zx)
            if abs(prueba.zz)>0:
                baseline = a*100/np.exp(2)+prueba.background/prueba.zz
                baseline1 = a*50+prueba.background/prueba.zz
                baseline2 = a*80+prueba.background/prueba.zz
            else:
                baseline = a*100/np.exp(2)+prueba.background
                baseline1 = a*50+prueba.background
                baseline2 = a*80+prueba.background
            x_x=int(len(s)/2)
            ss=s*prueba.pixel_size
            if abs(prueba.zz)>0:
                yy= a*np.exp(-2*(s/prueba.r_major)**2)+prueba.background/prueba.zz
            else:
                yy= a*np.exp(-2*(s/prueba.r_major)**2)+prueba.background
            yy=100*yy/max(yy)
            f_r=interp1d(yy[x_x:],ss[x_x:], kind='cubic', fill_value="extrapolate")
            prueba.rx1=abs(f_r(baseline))
            prueba.rx2=abs(f_r(baseline1))
            prueba.rx3=abs(f_r(baseline2))
            f_rdata1=interp1d(zx[int(x_x):],ss[x_x:], fill_value="extrapolate")
            f_rdata2=interp1d(zx[:x_x],ss[:x_x], fill_value="extrapolate")
            prueba.dimx1data=abs(f_rdata1(baseline))+abs(f_rdata2(baseline))
            prueba.dimx2data=abs(f_rdata1(baseline1))+abs(f_rdata2(baseline1))
            prueba.dimx3data=abs(f_rdata1(baseline2))+abs(f_rdata2(baseline2))
            _, _, zy, s = get_minor_axis_values(prueba.image, prueba.xc, prueba.yc, prueba.dx, prueba.dy, prueba.phi)
            #a = np.sqrt(2/np.pi)/prueba.r_minor * np.sum(zy-prueba.background)*abs(s[1]-s[0])
            zy=prueba.zy
            s=prueba.sy
            a = prueba.a
            if np.any(zy > 0):
                zy=100*zy/max(zy)
            if abs(prueba.zz)>0:
                baseline = a*100/np.exp(2)+prueba.background/prueba.zz
                baseline1 = a*50+prueba.background/prueba.zz
                baseline2 = a*80+prueba.background/prueba.zz
            else:
                baseline = a*100/np.exp(2)+prueba.background
                baseline1 = a*50+prueba.background
                baseline2 = a*80+prueba.background
            x_x=int(len(s)/2)
            ss=s*prueba.pixel_size
            if abs(prueba.zz)>0:
                yy= a*np.exp(-2*(s/prueba.r_minor)**2)+prueba.background/prueba.zz
            else:
                yy= a*np.exp(-2*(s/prueba.r_minor)**2)+prueba.background
            yy=100*yy/max(yy)
            f_r=interp1d(yy[x_x:],ss[x_x:], kind='cubic', fill_value="extrapolate")
            prueba.ry1=abs(f_r(baseline))
            prueba.ry2=abs(f_r(baseline1))
            prueba.ry3=abs(f_r(baseline2))
            f_rdata1=interp1d(zy[x_x:],ss[x_x:], fill_value="extrapolate")
            f_rdata2=interp1d(zy[:x_x],ss[:x_x], fill_value="extrapolate")
            prueba.dimy1data=abs(f_rdata1(baseline))+abs(f_rdata2(baseline))
            prueba.dimy2data=abs(f_rdata1(baseline1))+abs(f_rdata2(baseline1))
            prueba.dimy3data=abs(f_rdata1(baseline2))+abs(f_rdata2(baseline2))
            cx=2*[abs(prueba.rx1),abs(prueba.rx2),abs(prueba.rx3)]
            cy=2*[prueba.ry1,prueba.ry2,prueba.ry3]
            cox=[prueba.dimx1data,prueba.dimx2data,prueba.dimx3data]
            coy=[prueba.dimy1data,prueba.dimy2data,prueba.dimy3data]
            Ix=float('%.1g' % max(zx))
            Iy=float('%.1g' % max(zy))
            coaux1m=max(sum(cx),sum(cox))
            coaux1min=min(sum(cx),sum(cox))
            coauy1m=max(sum(cy),sum(coy))
            coauy1min=min(sum(cy),sum(coy))
            core1=100-100*abs(abs(coaux1m)-abs(coaux1min))/abs(sum(cx))
            core2=100-100*abs(abs(coauy1m)-abs(coauy1min))/abs(sum(cy))
            correla.append(core1+core2)
            valor.append(i)
        try:

            self.LaserData.background_fraction=valor[np.where(correla == max(correla))[0][0]]
            self.update_LaserData()
        except:
            pass
                                                                                                                                                                                                                                                                                                        
    def update_LaserData(self):
        self.LaserData=LaserData(self.LaserData.image1, self.LaserData.pixel_size,self.LaserData.units,self.LaserData.background_fraction)
        self.Semiminor=Semiminor(self.LaserData)
        self.Semimajor=Semimajor(self.LaserData)
    def data(self):
        datos=pd.DataFrame()
        cx=2*[abs(self.Semimajor.rx1),abs(self.Semimajor.rx2),abs(self.Semimajor.rx3)]
        cy=2*[self.Semiminor.ry1,self.Semiminor.ry2,self.Semiminor.ry3]
        cox=[self.Semimajor.dimx1data,self.Semimajor.dimx2data,self.Semimajor.dimx3data]
        coy=[self.Semiminor.dimy1data,self.Semiminor.dimy2data,self.Semiminor.dimy3data]
        coaux1m=max(sum(cx),sum(cox))
        coaux1min=min(sum(cx),sum(cox))
        coauy1m=max(sum(cy),sum(coy))
        coauy1min=min(sum(cy),sum(coy))
        if abs(sum(cx)) != 0:
            core1 = 100 - 100 * abs(abs(coaux1m) - abs(coaux1min)) / abs(sum(cx))
        else:
            core1 = 0  # Otra acción que desees realizar en caso de división por cero

        if abs(sum(cy)) != 0:
            core2 = 100 - 100 * abs(abs(coauy1m) - abs(coauy1min)) / abs(sum(cy))
        else:
            core2 = 0

        exent=np.sqrt(1-(min(self.Semimajor.rx1,self.Semiminor.ry1)**2)/(max(self.Semimajor.rx1,self.Semiminor.ry1)**2))
        datos["Attributes"]=["Width 13.5% (μm)","Width 50% (μm)","Width 80% (μm)","Intensity (%)","Centroid","Correlation (%)","resolution (px)","Eccentricity", "Pixel_size (μm)","φ(°)"]
        datos["semi-axis major beam"]=[str(round(self.Semimajor.dimx1data)),
                                    str(round(self.Semimajor.dimx2data)),
                                    str(round(self.Semimajor.dimx3data)),
                                    str(round(self.Semimajor.I.max()))+"%",
                                    str(round(self.LaserData.xc_s)),
                                    str(round(core1,2)),
                                    str(self.LaserData.image1.shape[0]),
                                    str(round(exent,2)),
                                    str(self.LaserData.pixel_size),
                                    str(round(self.LaserData.phi*180/np.pi,2))]
        datos["semi-axis minor beam"]=[str(round(self.Semiminor.dimy1data)),
                                    str(round(self.Semiminor.dimy2data)),
                                    str(round(self.Semiminor.dimy3data)),
                                    str(round(self.Semiminor.I.max()))+"%",
                                    str(round(self.LaserData.yc_s)),
                                    str(round(core2,2)),
                                    str(self.LaserData.image1.shape[1]),
                                    "",
                                    "",
                                    ""]
        datos["semi-axis major gaussian"]=[str(round(2*self.Semimajor.rx1)),
                                        str(round(2*self.Semimajor.rx2)),
                                        str(round(2*self.Semimajor.rx3)),
                                        "",
                                        "",
                                        "",
                                        "",
                                        "",
                                        "",
                                        ""]
        datos["semi-axis minor gaussian"]=[str(round(2*self.Semiminor.ry1)),
                                        str(round(2*self.Semiminor.ry2)),
                                        str(round(2*self.Semiminor.ry3)),
                                        "",
                                        "",
                                        "",
                                        "",
                                        "",
                                        "",
                                        ""]
        return datos

                










class LaserData:
    """
    Inicializa un objeto LaserData con información de la imagen y parámetros relacionados.

    Args:
        image (str or numpy.ndarray): Ruta de la imagen o matriz de la imagen.
        pixel_size (float): Tamaño de píxel en unidades específicas.
        units (str): Unidades de medida para los datos.
        background_fraction (float): Fracción del fondo a restar.
        crop (bool, optional): Indica si se debe recortar la imagen alrededor del haz. Por defecto, True.
    """
    def __init__(self,image, pixel_size,units,background_fraction,crop=False)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               :
        if type(image)==str:
            self.image=image
            o_image =cv2.imread(self.image)
        else:
            o_image=image
        self.image1=np.array(o_image)
        self.crop=crop
        self.pixel_size=pixel_size
        self.background_fraction=background_fraction
        self.units=units
        self.unit_str = '[%s]' % units
        self.label = 'Distancia desde el centro %s' % self.unit_str
        
        if(len(o_image.shape)<3):
            o_image
        elif len(o_image.shape)==3:
            o_image=cv2.cvtColor(o_image, cv2.COLOR_BGR2GRAY)
        self.image=o_image
        
        self.image=subtract_iso_background(self.image, background_fraction=self.background_fraction)
        #ret, thresh = cv2.threshold(self.image*2, int(np.max(self.image)*2*0.035), np.max(self.image)*2, cv2.THRESH_BINARY)
        #self.image[thresh < np.max(thresh)] = 0
        xc, yc, self.dx, self.dy, self.phi = measure_beam_size(o_image, max_iter=25)
        self.xc, self.yc= xc, yc
        if self.crop:
            self.image, self.xc, self.yc = crop_image_to_integration_rectangle(self.image, xc, yc, self.dx, self.dy, self.phi)
        
        vv, hh = self.image.shape
        scale=self.pixel_size
        
        self.min_ = self.image.min()
        self.max_ = self.image.max()
        self.r_major = max(self.dx, self.dy)/2.0
        self.r_minor = min(self.dx, self.dy)/2.0
        self.v_s = vv * scale
        self.h_s = hh * scale
        self.xc_s = self.xc * scale
        self.yc_s = self.yc * scale
        self.r_mag_s = self.r_major * scale
        self.d_mag_s = self.r_mag_s * 2
        self.r_min_s = self.r_minor * scale
        self.d_min_s = self.r_min_s * 2
        self.background, _ = determine_image_background(self.image)
        _, _, self.zy, self.sy = get_minor_axis_values(self.image, self.xc, self.yc, self.dx, self.dy, self.phi)
        _, _, self.zx, self.sx = get_major_axis_values(self.image, self.xc, self.yc, self.dx, self.dy, self.phi)
        self.zz=max(max(self.zy),max(self.zx))
        self.zy=self.zy.astype(float)/self.zz.astype(float)
        self.zx=self.zx.astype(float)/self.zz.astype(float)
        self.a=1
        

class LaserData:
    """
    Initialize a LaserData object with image information and related parameters.

    Args:
        image (str or numpy.ndarray): Path to the image or image matrix.
        pixel_size (float): Pixel size in specific units.
        units (str): Units of measurement for the data.
        background_fraction (float): Fraction of background to subtract.
        crop (bool, optional): Indicates whether to crop the image around the beam. Defaults to True.
    """
    def __init__(self, image, pixel_size, units, background_fraction, crop=False):
        if isinstance(image, str):
            self.image = image
            o_image = cv2.imread(self.image)
        else:
            o_image = image
        self.image1 = np.array(o_image)
        self.crop = crop
        self.pixel_size = pixel_size
        self.background_fraction = background_fraction
        self.units = units
        self.unit_str = '[%s]' % units
        self.label = 'Distance from center %s' % self.unit_str

        if len(o_image.shape) < 3:
            o_image
        elif len(o_image.shape) == 3:
            o_image = cv2.cvtColor(o_image, cv2.COLOR_BGR2GRAY)
        self.image = o_image
        
        self.image = subtract_iso_background(self.image, background_fraction=self.background_fraction)
        self.mean=self.image.mean()
        self.std=self.image.std()
        ret, thresh = cv2.threshold(self.image * 2, int(np.max(self.image) * 2 * 0.035), np.max(self.image) * 2, cv2.THRESH_BINARY)
        self.image[thresh < np.max(thresh)] = 0
        xc, yc, self.dx, self.dy, self.phi = measure_beam_size(o_image, max_iter=25)
        self.xc, self.yc = xc, yc
        if self.crop:
            self.image, self.xc, self.yc = crop_image_to_integration_rectangle(self.image, xc, yc, self.dx, self.dy, self.phi)

        vv, hh = self.image.shape
        scale = self.pixel_size

        self.min_ = self.image.min()
        self.max_ = self.image.max()
        self.r_major = max(self.dx, self.dy) / 2.0
        self.r_minor = min(self.dx, self.dy) / 2.0
        self.v_s = vv * scale
        self.h_s = hh * scale
        self.xc_s = self.xc * scale
        self.yc_s = self.yc * scale
        self.r_mag_s = self.r_major * scale
        self.d_mag_s = self.r_mag_s * 2
        self.r_min_s = self.r_minor * scale
        self.d_min_s = self.r_min_s * 2
        self.background, _ = determine_image_background(self.image)
        _, _, self.zy, self.sy = get_minor_axis_values(self.image, self.xc, self.yc, self.dx, self.dy, self.phi)
        _, _, self.zx, self.sx = get_major_axis_values(self.image, self.xc, self.yc, self.dx, self.dy, self.phi)
        self.zz = max(max(self.zy), max(self.zx))
        if self.zz != 0:
            self.zy = self.zy.astype(float) / self.zz.astype(float)
            self.zx = self.zx.astype(float) / self.zz.astype(float)
        else:
            # Set the numerator to zero when denominator is zero
            self.zy = self.zy
            self.zx = self.zx
        self.a = 1
        


class Semiminor:
    """
    Initialize a Semiminor object with data related to the minor dimension of the beam.

    Args:
        LaserData (LaserData): LaserData object from which data is obtained for calculation.
    """
    def __init__(self, LaserData):
        zy = LaserData.zy
        s = LaserData.sy
        a = 1

        if max(zy) != 0:
            zy = 100 * zy / max(zy)
            
        if LaserData.zz != 0:
            baseline = a * 100 / np.exp(2) + LaserData.background / LaserData.zz
            baseline1 = a * 50 + LaserData.background / LaserData.zz
            baseline2 = a * 80 + LaserData.background / LaserData.zz
        else:
            baseline = a * 100 / np.exp(2) + LaserData.background 
            baseline1 = a * 50 + LaserData.background 
            baseline2 = a * 80 + LaserData.background 
            
        self.ss = s * LaserData.pixel_size
        # Remove duplicate values from yy and keep corresponding ss values
        self.ss, unique_indices = np.unique(self.ss, return_index=True)
        zy = zy[unique_indices]
        x_x = int(len(s) / 2)
        
        if LaserData.zz != 0:
            if LaserData.r_minor != 0:
                yy = a * np.exp(-2 * (s / LaserData.r_minor) ** 2) + LaserData.background / LaserData.zz
            else:
                yy = a * np.exp(-2 * s) + LaserData.background / LaserData.zz
        else:
            if LaserData.r_minor != 0:
                yy = a * np.exp(-2 * (s / LaserData.r_minor) ** 2) + LaserData.background
            else:
                yy = a * np.exp(-2 * s) + LaserData.background
        
        if max(yy) != 0: 
            yy = 100 * yy / max(yy)
        
        self.I = yy
        
        print(LaserData.mean)
        
        if LaserData.mean > 0.095:
            if len(yy) != len(self.ss):
                self.ry1 = abs(LaserData.d_min_s)
                self.ry2 = abs(LaserData.d_min_s * 0.4)
                self.ry3 = abs(LaserData.d_min_s * 0.19)
                self.dimy1data = abs(LaserData.r_min_s) * 0.45 + abs(LaserData.r_min_s * 0.47)
                self.dimy2data = abs(LaserData.r_min_s * 0.4) * 0.45 + abs(LaserData.r_min_s * 0.4 * 0.47)
                self.dimy3data = abs(LaserData.r_min_s * 0.19) * 0.45 + abs(LaserData.r_min_s * 0.19 * 0.47)
            else:
                # Los arrays no están vacíos, se pueden pasar a interp1d
                f_r = interp1d(yy[x_x:], self.ss[x_x:], kind='cubic', fill_value="extrapolate")
                
                self.ry1 = abs(f_r(baseline))
                self.ry2 = abs(f_r(baseline1))
                self.ry3 = abs(f_r(baseline2))
                
                self.f_rdata1 = interp1d(zy[x_x:], self.ss[x_x:], fill_value="extrapolate")
                self.f_rdata2 = interp1d(zy[:x_x], self.ss[:x_x], fill_value="extrapolate")
                self.dimy1data = abs(self.f_rdata1(baseline)) + abs(self.f_rdata2(baseline))
                self.dimy2data = abs(self.f_rdata1(baseline1)) + abs(self.f_rdata2(baseline1))
                self.dimy3data = abs(self.f_rdata1(baseline2)) + abs(self.f_rdata2(baseline2))
        elif LaserData.mean < 0.095:
            self.ry1 = abs(LaserData.d_min_s)
            self.ry2 = abs(LaserData.d_min_s * 0.4)
            self.ry3 = abs(LaserData.d_min_s * 0.19)
            self.dimy1data = abs(LaserData.r_min_s) * 0.45 + abs(LaserData.r_min_s * 0.47)
            self.dimy2data = abs(LaserData.r_min_s * 0.4) * 0.45 + abs(LaserData.r_min_s * 0.4 * 0.47)
            self.dimy3data = abs(LaserData.r_min_s * 0.19) * 0.45 + abs(LaserData.r_min_s * 0.19 * 0.47)
        else:
            self.ry1 = abs(LaserData.d_min_s)
            self.ry2 = abs(LaserData.d_min_s * 0.4)
            self.ry3 = abs(LaserData.d_min_s * 0.19)
            self.dimy1data = abs(LaserData.r_min_s) * 0.45 + abs(LaserData.r_min_s * 0.47)
            self.dimy2data = abs(LaserData.r_min_s * 0.4) * 0.45 + abs(LaserData.r_min_s * 0.4 * 0.47)
            self.dimy3data = abs(LaserData.r_min_s * 0.19) * 0.45 + abs(LaserData.r_min_s * 0.19 * 0.47)
            
            


class Semimajor:
    """
    Initialize a Semimajor object with data related to the major dimension of the beam.

    Args:
        LaserData (LaserData): LaserData object from which data is obtained for calculation.
    """
    def __init__(self, LaserData):
        zx = LaserData.zx
        s = LaserData.sx
        a = 1
        
        if max(zx)!=0:
            zx = 100 * zx / max(zx)
        if LaserData.zz!=0:
            baseline = a * 100 / np.exp(2) + LaserData.background / LaserData.zz
            baseline1 = a * 50 + LaserData.background / LaserData.zz
            baseline2 = a * 80 + LaserData.background / LaserData.zz
        else:
            baseline = a * 100 / np.exp(2) + LaserData.background 
            baseline1 = a * 50 + LaserData.background 
            baseline2 = a * 80 + LaserData.background 
        self.ss = s * LaserData.pixel_size
        # Remove duplicate values from yy and keep corresponding ss values
        self.ss, unique_indices = np.unique(self.ss, return_index=True)
        zx = zx[unique_indices]
        
        x_x = int(len(s) / 2)
        
        
        
        if abs(LaserData.zz)>0.0:
            if LaserData.r_major!=0.0:
                self.yy = a * np.exp(-2 * (s / LaserData.r_major) ** 2) + LaserData.background / LaserData.zz
            else:
                self.yy = a * np.exp(-2 * (s ) ** 2) + LaserData.background / LaserData.zz
        else:
            if LaserData.r_major!=0.0:
                self.yy = a * np.exp(-2 * (s / LaserData.r_major) ** 2) + LaserData.background 
            else:
                self.yy = a * np.exp(-2 * (s ) ** 2) + LaserData.background 
        self.yy=self.yy[unique_indices]
        mask = np.isnan(self.yy)
        
        if mask.any():
            sx = self.yy[~mask]
            if sx.size == 0:
                print("No Sirve !!")
        if max(self.yy)!=0:
            self.yy = 100 * self.yy / max(self.yy)
        self.I = self.yy
        print(LaserData.mean)
        if LaserData.mean > 0.095:
            if len(self.yy[x_x:]) > 0 and len(self.ss[x_x:]) > 0:
                # Los arrays no están vacíos, se pueden pasar a interp1d
                f_r = interp1d(self.yy[x_x:], self.ss[x_x:], kind='cubic', fill_value="extrapolate")
            
                self.rx1 = abs(f_r(baseline))
                self.rx2 = abs(f_r(baseline1))
                self.rx3 = abs(f_r(baseline2))
                
                self.f_rdata1 = interp1d(zx[int(x_x):], self.ss[x_x:], fill_value="extrapolate")
                self.f_rdata2 = interp1d(zx[:x_x], self.ss[:x_x], fill_value="extrapolate")
                self.dimx1data = abs(self.f_rdata1(baseline)) + abs(self.f_rdata2(baseline))
                self.dimx2data = abs(self.f_rdata1(baseline1)) + abs(self.f_rdata2(baseline1))
                self.dimx3data = abs(self.f_rdata1(baseline2)) + abs(self.f_rdata2(baseline2))
            else:
                # Manejar el caso cuando los arrays están vacíos
                self.rx1 = abs(LaserData.d_mag_s )
                self.rx2 = abs(LaserData.d_mag_s*0.4)
                self.rx3 = abs(LaserData.d_mag_s*0.19)
                self.dimx1data = abs(LaserData.r_mag_s)*0.45 + abs(LaserData.r_mag_s*0.47)
                self.dimx2data = abs(LaserData.r_mag_s*0.4)*0.45 + abs(LaserData.r_mag_s*0.4*0.47)
                self.dimx3data = abs(LaserData.r_mag_s*0.19)*0.45 + abs(LaserData.r_mag_s*0.19*0.47)
        elif LaserData.mean > 0.095:
            self.rx1 = 0
            self.rx2 = 0
            self.rx3 = 0
            self.dimx1data = 0
            self.dimx2data = 0
            self.dimx3data = 0
        else:
            self.rx1 = abs(LaserData.d_mag_s )
            self.rx2 = abs(LaserData.d_mag_s*0.4)
            self.rx3 = abs(LaserData.d_mag_s*0.19)
            self.dimx1data = abs(LaserData.r_mag_s)*0.45 + abs(LaserData.r_mag_s*0.47)
            self.dimx2data = abs(LaserData.r_mag_s*0.4)*0.45 + abs(LaserData.r_mag_s*0.4*0.47)
            self.dimx3data = abs(LaserData.r_mag_s*0.19)*0.45 + abs(LaserData.r_mag_s*0.19*0.47)
        
