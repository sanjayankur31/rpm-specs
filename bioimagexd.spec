# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global svn_rev 1721

Name:           bioimagexd
Version:        20110709
Release:        0.1svn%{svn_rev}%{?dist}
Summary:        Software for analysis and visualization of multidimensional biomedical images

License:        GPL
URL:            http://sourceforge.net/projects/bioimagexd
# svn export
# https://bioimagexd.svn.sourceforge.net/svnroot/bioimagexd/bioimagexd/trunk/ bioimagexd
# tar -cvzf bioimagexd-20110709.tar.gz bioimagexd/
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python-devel vtk-devel cmake
# from rpmfusion
# Requires:       ffmpeg 
Requires:       wxPython

%description
Features:
== Image Viewing ==

Open data in common microscopy formats (or images or stacks of images, and time
series), and view the data image by image. Supported data formats include:

    Carl Zeiss .lsm files
    OlympusFV1000 .oif
    Leica confocal microscope data files SP2 .txt and SP5 .lif
    numbered image stacks import
    VTK XML Image files
 

Image viewing is roughly comparable to the free Carl Zeiss, Olympus, Leica and
other commercial image viewers, but with very realistic 3D rendering without
artifacts from the graphics card - using ray cast 3D mode.  Viewing modes
avaialble are: Slices, orthographic sections, maximum intensity projection and
3D rendering. Time series data are supported.

== Image processing ==

Adjust colour / brightness / contrast / gamma, change colour or palette of a
dataset/channel, filter out noise, correct for fluorescence bleaching in time
series data.

3D segmentation and object ananlysis.  
3D volume rendering     

3D datasets can be interactively volume rendered, using

    software ray casting (slower but prettiest. Acellerated by having many
processors)
    OpenGL graphics card texture mapping (faster but lower resolution -
depending on texture menory size)
    TeraRecon Inc. VolumePro1000 hardware ray casting board (support in
development)

 
The colour and opacity transfer functions are fully user defined. You can volume
render a merged multi channel RGB dataset to see colocalisation in 3D, or render
a 3D colocalisation map. BioImageXD uses the VTK interface with OpenGL. We plan
to enable Hardware Stereo viewing (quad buffered page flipping and red-blue
anaglyph, and other modes). You will be able to break out those 3D glasses and
really "see" your data! This is the future of 3D microscopy.

== Movie making ==

Use the Animator module to set up a camera path around your 3D data, and make a
movie of it spinning and fly though zooming any way you like. Time series data
are supported: "4D data".
Colocalisation analysis     

We know all you cell biologists using confocal microscopy are always looking for
colocalisation! Our colocalisation tool allows you to analyse the colocalisation
of signal intensity in a multi channel 3D data set, avoiding the problem of
false colocalisation seen in z-stack projection images, and perform some
statistical analyses that give you hard numbers about the amount and quality of
colocalisation in your data. Uses similar algorithms to those in imageJ, for
instance the WCIF plugin for Automatic Colocalisation Thresholds, using the
method of Costes et al.

Manders coefficients and statistical significance analysis, with 2D
histogram/scatterplot and results statistics export 


%prep
%setup -q -n %{name}
rm -rvf bin/


%build
pushd ./vtkBXD/
    export VTK_DIR="%{_libdir}/vtk-5.6/"
    export ITK_DIR="%{_libdir}/InsightToolkit/"
    export VTKBXD_WRAP_PYTHON=ON
    %cmake .
    make && make install
popd

pushd ./itkBXD/
    export VTK_DIR="%{_libdir}/vtk-5.6/"
    export ITK_DIR="%{_libdir}/InsightToolkit/"
    export VTKBXD_WRAP_PYTHON=ON
    %cmake .
    make && make install
popd

# Remove CFLAGS=... for noarch packages (unneeded)
# CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
make


%install
rm -rf $RPM_BUILD_ROOT
#%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT 

%files 
%doc 
# For noarch packages: sitelib %{python_sitelib}/* 
# For arch-specific packages: sitearch %{python_sitearch}/* 

%changelog 
* Sat Jul 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110709-0.1svn1721 - initial rpm build
