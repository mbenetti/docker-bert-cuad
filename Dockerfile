FROM python:3.8.0

# Copy local code to the container image.
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt \
	&& rm -rf requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["main.py"]