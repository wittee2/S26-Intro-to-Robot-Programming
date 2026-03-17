from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'test_tf2_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='test_tf2_py package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_tf2_broadcaster = test_tf2_py.turtle_tf2_broadcaster:main',
            'turtle_tf2_listener = test_tf2_py.turtle_tf2_listener:main',
            'fixed_frame_tf2_broadcaster = test_tf2_py.fixed_frame_tf2_broadcaster:main',
            'dynamic_frame_tf2_broadcaster = test_tf2_py.dynamic_frame_tf2_broadcaster:main',
        ],
    },
)
