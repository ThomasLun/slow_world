FROM python:3.7.3-alpine3.9
ENV APP_NAME ordercenter

ADD requirements.txt /
RUN apk add --no-cache gcc libc-dev git libffi-dev make openssl-dev \
    && pip install --upgrade pip \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt --no-cache-dir \
    &&rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache /usr/libexec/git-core /usr/libexec/gcc




EXPOSE 8000

WORKDIR /$APP_NAME



CMD ["python", "main.py", "8000"]