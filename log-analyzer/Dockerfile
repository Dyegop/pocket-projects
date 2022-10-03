FROM python:3.9

# set the working directory
RUN mkdir -p /log-analyzer
WORKDIR /log-analyzer

# copy the scripts to the folder
COPY . /log-analyzer

# set entry point
ENTRYPOINT ["python", "main_log_analyzer.py", "/log-analyzer/input/access.log"]
