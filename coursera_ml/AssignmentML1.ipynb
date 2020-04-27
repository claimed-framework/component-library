{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This is the first assignment for the Coursera course \"Advanced Machine Learning and Signal Processing\"\n",
    "\n",
    "Just execute all cells one after the other and you are done - just note that in the last one you have to update your email address (the one you've used for coursera) and obtain a submission token, you get this from the programming assignment directly on coursera."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This notebook is designed to run in a IBM Watson Studio default runtime (NOT the Watson Studio Apache Spark Runtime as the default runtime with 1 vCPU is free of charge). Therefore, we install Apache Spark in local mode for test purposes only. Please don't use it in production.\n",
    "\n",
    "In case you are facing issues, please read the following two documents first:\n",
    "\n",
    "https://github.com/IBM/skillsnetwork/wiki/Environment-Setup\n",
    "\n",
    "https://github.com/IBM/skillsnetwork/wiki/FAQ\n",
    "\n",
    "Then, please feel free to ask:\n",
    "\n",
    "https://coursera.org/learn/machine-learning-big-data-apache-spark/discussions/all\n",
    "\n",
    "Please make sure to follow the guidelines before asking a question:\n",
    "\n",
    "https://github.com/IBM/skillsnetwork/wiki/FAQ#im-feeling-lost-and-confused-please-help-me\n",
    "\n",
    "\n",
    "If running outside Watson Studio, this should work as well. In case you are running in an Apache Spark context outside Watson Studio, please remove the Apache Spark setup in the first notebook cells."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from IPython.display import Markdown, display\n",
    "def printmd(string):\n",
    "    display(Markdown('# <span style=\"color:red\">'+string+'</span>'))\n",
    "\n",
    "\n",
    "if ('sc' in locals() or 'sc' in globals()):\n",
    "    printmd('<<<<<!!!!! It seems that you are running in a IBM Watson Studio Apache Spark Notebook. Please run it in an IBM Watson Studio Default Runtime (without Apache Spark) !!!!!>>>>>')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install pyspark==2.4.5"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "try:\n",
    "    from pyspark import SparkContext, SparkConf\n",
    "    from pyspark.sql import SparkSession\n",
    "except ImportError as e:\n",
    "    printmd('<<<<<!!!!! Please restart your kernel after installing Apache Spark !!!!!>>>>>')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "sc = SparkContext.getOrCreate(SparkConf().setMaster(\"local[*]\"))\n",
    "\n",
    "spark = SparkSession \\\n",
    "    .builder \\\n",
    "    .getOrCreate()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!wget https://github.com/IBM/coursera/raw/master/coursera_ml/a2.parquet"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df=spark.read.load('a2.parquet')\n",
    "\n",
    "df.createOrReplaceTempView(\"df\")\n",
    "spark.sql(\"SELECT * from df\").show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!rm -Rf a2_m1.json"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = df.repartition(1)\n",
    "df.write.json('a2_m1.json')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!rm -f rklib.py\n",
    "!wget https://raw.githubusercontent.com/IBM/coursera/master/rklib.py"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import zipfile\n",
    "import os\n",
    "\n",
    "def zipdir(path, ziph):\n",
    "    for root, dirs, files in os.walk(path):\n",
    "        for file in files:\n",
    "            ziph.write(os.path.join(root, file))\n",
    "\n",
    "zipf = zipfile.ZipFile('a2_m1.json.zip', 'w', zipfile.ZIP_DEFLATED)\n",
    "zipdir('a2_m1.json', zipf)\n",
    "zipf.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "!base64 a2_m1.json.zip > a2_m1.json.zip.base64"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from rklib import submit\n",
    "key = \"1injH2F0EeiLlRJ3eJKoXA\"\n",
    "part = \"wNLDt\"\n",
    "email = \"###YOUR_CODE_GOES_HERE###\"\n",
    "token = \"###YOUR_CODE_GOES_HERE###\" #(have a look here if you need more information on how to obtain the token https://youtu.be/GcDo0Rwe06U?t=276)\n",
    "\n",
    "with open('a2_m1.json.zip.base64', 'r') as myfile:\n",
    "    data=myfile.read()\n",
    "submit(email, token, key, part, [part], data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3.6",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
