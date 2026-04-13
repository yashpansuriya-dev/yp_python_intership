# prebuilt base image
FROM apify/actor-python-playwright

# switch from root user(full control) to non root user (limited access)
USER myuser

# copy reuirements.txt
#             owner:group
             # |     |
COPY --chown=myuser:myuser requirements.txt ./

# install all dependencies
RUN pip install -r requirements.txt

COPY --chown=myuser:myuser . ./

# complied specied file
RUN python -m compileall -q my_actor/

#run 
CMD ["python","-m", "my_actor"]