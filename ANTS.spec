%global svn_rev 942
%global checkout_date 20110813

Name:           ANTS
Version:        1.9.x
Release:        1.%{checkout_date}.svn%{svn_rev}%{?dist}
Summary:        Advanced Normalization Tools

License:        BSD
URL:            http://www.picsl.upenn.edu/ANTS/

# svn export -r %{svn_rev} https://advants.svn.sourceforge.net/svnroot/advants ANTS
# tar -cvzf %{name}-%{checkout_date}.tar.gz %{name}/
Source0:        %{name}-%{checkout_date}.tar.gz

BuildRequires:  cmake 
BuildRequires:  InsightToolkit-devel

%description
ANTS is a tool for computational neuroanatomy based on medical 
images. ANTS reads any image type that can be read by 
ITK (www.itk.org), that is, jpg, tiff, hdr, nii, nii.gz, mha/d 
and more image types as well. For the most part, ANTS will output 
float images which you can convert to other types with the ANTS 
ConvertImagePixelType tool. ImageMath has a bunch of basic 
utilities such as multiplication, inversion and many more advanced 
tools such as computation of the Lipschitz norm of a deformation 
field. ANTS programs may be called from the command line on almost 
any platform .... you can compile the code yourself or use the 
precompiled binaries for Windows (Vista), OSX (Darwin) or linux 
(32 bit or 64 bit). Download the binaries that are correct for you. 
If you are a naive user (not from a medical imaging background) 
then you might still find the tools here useful. Many of the 
operations available, for instance, in PhotoShop are available in 
ANTS and many more are available as well. For instance, ANTS tools 
may be useful in face mapping / morphing and also in generating 
animations from two different images, for instance, interpolating 
between frames in a movie. But, mainly, ANTS is useful for brain 
mapping, segmentation, measuring cortical thickness and in 
generating automated or semi-automated labeling of 
three-dimensional imagery (e.g. labeling hippocampus or cortical 
regions or lobes of the lung). Many prior-based segmentation 
possibilities are available in the Atropos tool, including three 
tissue segmentation, structure-specific segmentation and brain 
extracton.


%prep
%setup -q -n %{name}


%build
%cmake -DBUILD_TYPE=RELEASE


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc



%changelog
* Sat Aug 13 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.9.x-1.20110813.svn942
- Initial rpm build
