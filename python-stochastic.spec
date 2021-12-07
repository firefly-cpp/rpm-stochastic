%bcond_without tests

# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
# It is disabled for now (problems with svg graphics)
%bcond_with doc_pdf

%global pypi_name stochastic

%global _description %{expand:
This package offers a number of common discrete-time, continuous-time,
and noise process objects for generating realizations of stochastic
processes as numpy arrays. The diffusion processes are approximated
using the Euler–Maruyama method.}

Name:           python-%{pypi_name}
Version:        0.6.0
Release:        1%{?dist}
Summary:        Generate realizations of stochastic processes in python

License:        MIT
URL:            https://github.com/crflynn/%{pypi_name}
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz

# https://github.com/crflynn/stochastic/pull/63
Patch0:         63a.patch

BuildArch:      noarch

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-xdist}
BuildRequires:  %{py3_dist codecov}
BuildRequires:  %{py3_dist pytest-cov}
%endif

%description -n python3-%{pypi_name} %_description

%package doc
Summary:        %{summary}

%if %{with doc_pdf}
BuildRequires:  make
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-rtd-theme}
%endif

%description doc
Documentation for %{name}.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
rm -rf poetry.lock

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%if %{with doc_pdf}
%make_build -C docs latex SPHINXOPTS='%{?_smp_mflags}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif

%install
%pyproject_install
%pyproject_save_files stochastic

%check
%if %{with tests}
%pytest
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE.txt
%doc README.rst CHANGELOG.rst

%files doc
%license LICENSE.txt
%if %{with doc_pdf}
%doc docs/_build/latex/%{pypi_name}.pdf
%endif


%changelog
* Tue Dec 7 2021 Iztok Fister Jr. <iztokf AT fedoraproject DOT org> - 0.6.0-1
- Initial package
