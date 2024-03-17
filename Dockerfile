FROM ubuntu:noble

RUN apt-get update
RUN apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev software-properties-common libpq-dev libkrb5-dev python3-dev git dos2unix
RUN apt-get update
RUN apt-get install -y sudo openssh-client
RUN update-ca-certificates

ENV HOME="/root"
WORKDIR ${HOME}

RUN echo "[global]\
trusted-host = pypi.python.org\
               pypi.org\
               eos2git.cec.lab.emc.com\
               files.pythonhosted.org" >  /etc/pip.conf

RUN useradd -d /home/circleci -m circleci
RUN usermod -aG sudo circleci
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER circleci
WORKDIR /home/circleci
ENV HOME="/home/circleci"

RUN git config --global http.sslVerify false
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="/home/circleci/.local/bin:${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

ENV PYTHON_VERSION=3.11.1
RUN pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}

RUN git clone https://github.com/pyenv/pyenv-virtualenv.git ${PYENV_ROOT}/plugins/pyenv-virtualenv
RUN pip3 install --upgrade pip
RUN pip3 install --user virtualenv tox pip-tools setuptools
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
# RUN pip3 install https://github.com/cloudify-incubator/cloudify-ecosystem-test/archive/latest.zip
COPY setup.py setup.py
COPY ne_lint/ ne_lint
RUN sudo chown -R circleci:circleci ne_lint
RUN pip3 install -e .

WORKDIR /project

ENV GIT_CONFIG_COUNT=1
ENV GIT_CONFIG_KEY_0=safe.directory
ENV GIT_CONFIG_VALUE_0=*

ENTRYPOINT [ "/bin/bash", "ne-lint"]
