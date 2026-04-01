from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="artiq_ablation_camera",
    install_requires=required,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aqctl_artiq_ablation_camera = artiq_ablation_camera.aqctl_artiq_ablation_camera:main",
        ],
    },
)