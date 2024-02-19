# Beamdiameter: Software for Laser Beam Profile Analysis

Beamdiameter is an open-source and free software designed for laser beam characterization. Based on the ISO-11146 standard, Beamdiameter offers a flexible and powerful platform for efficiently and accurately analyzing laser beam profiles.

## Key Features:

1. **Real-Time Acquisition:**
   - Beamdiameter allows real-time acquisition of the laser beam profile. This means it can capture and process laser beam data as it is being generated, which is useful for experiments and applications requiring continuous monitoring.

2. **Camera Compatibility:**
   - The software is compatible with both generic cameras and Pyueye brand cameras. This provides flexibility in choosing the camera for laser beam image acquisition.

3. **Expansion of Camera Brands:**
   - Future versions plan to add support for more camera brands with Python APIs. This will expand the camera options available to users and ensure software compatibility with a variety of devices.

## Additional Benefits:

- **MIT License:**
   - Beamdiameter is distributed under the MIT license, allowing users to use, modify, and redistribute the software freely for both commercial and non-commercial projects. This license promotes collaboration and community development by providing a solid and open foundation for future improvements and customizations.

- **Written in Python:**
   - Python is a widely-used programming language known for its simplicity and versatility. As Beamdiameter is written in Python, users can leverage its extensive ecosystem of libraries and tools to tailor the software to their specific needs.

With its real-time acquisition capability, compatibility with various cameras, and focus on accessibility and flexibility through open-source code, the MIT license, and the ISO-11146 standard, Beamdiameter stands out as a powerful tool for laser beam characterization in a variety of experimental environments and industrial applications.
# Installation Instructions:
```bash
# After creating your virtual environment and activating it,
# you can install the required libraries using the following command:
pip install -r requirements.txt
```
## To run the software, execute the following command:
```bash
python3 main.py
```
## Additional Instructions for uEye Cameras:

If you plan to use a uEye camera, you'll need to install the camera drivers, which can be found on the official uEye website. Additionally, you'll need to install Pyueye, which is the Python API for uEye cameras. Please note that we are not affiliated with uEye; we simply contribute to the community.

To use a uEye camera, ensure that the attribute `self.typecamera` in `VideoThread` within the `main.py` file is set to "Ueye".

```bash
self.typecamera="Ueye"
```
## Compatibility:
This software version is compatible with Python 3.9, 3.10, 3.11, and 3.12.

**References:**

- ISO 11146-1:2021(en): "ISO 11146-1:2021(en) Lasers and laser-related equipment — Test methods for laser beam widths, divergence angles and beam propagation ratios — Part 1: Stigmatic and simple astigmatic beams". ISO. [Link](https://www.iso.org/obp/ui/#iso:std:iso:11146:-1:ed-2:v1:en)

- Scott Prahl. "ISO 11146 Calculation of Laser Beam Center, Diameter, and M2". ISO. [Link](https://pypi.org/project/laserbeamsize/)

