# base image
FROM deeppavlov/base-cpu
# copy to dir
COPY . /app
# use workdir
WORKDIR /app
# install requirements
RUN pip install -r requirements.txt
# expose port
EXPOSE 9009
# command to run
CMD ["python", "main.py"]
