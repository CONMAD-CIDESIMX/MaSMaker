# MaSMaker
An Open-Source, Portable Software to Create and Integrate Maze-like Surfaces into Arbitrary Geometries

MaSMaker aims to provide an easy-to-use and self-contained tool to embed geometrically customized TPMS-based structures into CAD models with an arbitrary geometry. The software is distributed in two different ways. The first distribution consists on the source code for the generation of TPMS structures using the Python programming language. The main distribution corresponds to a portable, executable file in which all the required libraries and packages have been included. This distribution has an easy-to-use GUI in order to facilitate the manipulation and integration of TPMS structures into arbitrary geometries represented by a STL file. In the Figure below is illustrated the workflow of the executable version of MaSMaker. After launching the application, the user must choose the geometry from one of the four available tabs. Three basic geometries are included, whereas the fourth option allows the user to work with an external geometry via a STL file. When using an external geometry, the user must ensure that the selected STL file is defect-free, since common mesh errors (such as non-manifold edges, overlapping triangles or inverted normals) can result in unexpected crash of the software  while performing the operations. At this point, the user has several options (commercial and free-to-use) to fix STL files and then input the repaired STL files into MaSMaker.

<img src="https://user-images.githubusercontent.com/89549378/178032184-0831dd82-d7d7-41b9-9e18-a4003de2174e.png" width="460" height="500">

The software tool allows to control the main parameters of TPMS structures (isovalue, cell resolution and unit cell size). MaSMaker is distributed under the GPLv3 license.

Executable version can be found in the release MaSMaker v1.0 (https://github.com/CONMAD-CIDESIMX/MaSMaker/releases/tag/v1.0)

For downloading the free license file key, follow the instructions in: Instructions to download MaSMaker license key.pdf
