# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='student_sys',
    version='0.1',
    description='Blog System base on Django',
    author='Fnanshan',
    author_email='20185584@stu.ccut.edu.cn',
    url='118.89.230.188',
    license='MIT',

    # 要打入的包
    packages=find_packages('student_sys'),
    # packages的包在哪个目录下，如果在setup.py同级目录，则可以不写
    package_dir={'': 'student_sys'},
    # 除了.py文件，还需要打包哪些文件到最终的安装包里。
    package_data={'': [             # 方法一：打包数据文件
        'student_sys/themes/*/*/*/*',           # 需要按目录层级匹配
    ]},
    # include_package_data=True,    # 方法二：配合MANIFEST.in文件
    # 指明依赖版本
    install_requires=[
        'django~=2.1.7',
    ],
    # 额外依赖
    extras_require={
        'ipython': ['ipython==7.16.3']
    },

    # 放到bin目录下的可执行文件
    scripts=[
        'student_sys/manage.py',
    ],
    # 程序执行的点（入口点）
    entry_points={
        'console_scripts': [        # 生成一个student_manage可执行文件到bin目录下，执行此命令就相当于执行了manage.py中的main()
            'student_manage = manage:main',
        ]
    },
    # 项目当前状况
    classifiers=[
        # 软件成熟度
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # 项目受众
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # 项目许可证
        'License :: OSI Approved :: MIT License',

        # 项目需要的Python版本
        'Programming Language :: Python :: 3.7.5',
    ],

)