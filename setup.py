from setuptools import setup, find_packages

setup(
    name='RickAndMortyDataFetcher',
    version='1.0.0', 
    author='David Espejo',
    author_email='davas.espejo@gmail.com',
    description='Una aplicación de Tkinter para consultar, filtrar y descargar datos de la API de Rick and Morty.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tuusuario/tu-repositorio',  # URL del repositorio del proyecto
    packages=find_packages('src'), 
    package_dir={'': 'src'},  # Directorio base para el código fuente
    classifiers=[
        'Programming Language :: Python :: 3',  # Versión de Python
        'License :: OSI Approved :: MIT License',  # Licencia
        'Operating System :: OS Independent',  # Sistema operativo
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
    install_requires=[  # Dependencias del proyecto
        'requests',
        'Pillow',
        'fastapi'
    ],
    extras_require={
        'dev': [
            'uvicorn[standard]'
        ],
    },

    entry_points={
        'console_scripts': [
            'rickandmorty=src.main:main',  
        ],
    },
)
