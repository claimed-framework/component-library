{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Exercise 2\n",
    "## Part 1\n",
    "Now let's calculate covariance and correlation by ourselves using ApacheSpark\n",
    "\n",
    "1st we crate two random RDD’s, which shouldn't correlate at all.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Waiting for a Spark session to start...\n",
      "Spark Initialization Done! ApplicationId = app-20190311213801-0000\n",
      "KERNEL_ID = ad8b051e-eb20-41ff-80d6-cc41afd5724e\n"
     ]
    }
   ],
   "source": [
    "import random\n",
    "rddX = sc.parallelize(random.sample(range(100),100))\n",
    "rddY = sc.parallelize(random.sample(range(100),100))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now we calculate the mean, note that we explicitly cast the denominator to float in order to obtain a float instead of int"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "49.5\n",
      "49.5\n"
     ]
    }
   ],
   "source": [
    "meanX = rddX.sum()/float(rddX.count())\n",
    "meanY = rddY.sum()/float(rddY.count())\n",
    "print (meanX)\n",
    "print (meanY)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now we calculate the covariance"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "-50.96"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "rddXY = rddX.zip(rddY)\n",
    "covXY = rddXY.map(lambda x_y : (x_y[0]-meanX)*(x_y[1]-meanY)).sum()/rddXY.count()\n",
    "covXY"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Covariance is not a normalized measure. Therefore we use it to calculate correlation. But before that we need to calculate the indivicual standard deviations first"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "28.86607004772212\n",
      "28.86607004772212\n"
     ]
    }
   ],
   "source": [
    "from math import sqrt\n",
    "n = rddXY.count()\n",
    "sdX = sqrt(rddX.map(lambda x : pow(x-meanX,2)).sum()/n)\n",
    "sdY = sqrt(rddY.map(lambda x : pow(x-meanY,2)).sum()/n)\n",
    "print (sdX)\n",
    "print (sdY)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now we calculate the correlation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "-0.06115811581158116"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "corrXY = covXY / (sdX * sdY)\n",
    "corrXY"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Part 2\n",
    "No we want to create a correlation matrix out of the four RDDs used in the lecture"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[[ 1.          1.         -1.          0.06967897]\n",
      " [ 1.          1.         -1.          0.06967897]\n",
      " [-1.         -1.          1.         -0.06967897]\n",
      " [ 0.06967897  0.06967897 -0.06967897  1.        ]]\n"
     ]
    }
   ],
   "source": [
    "from pyspark.mllib.stat import Statistics\n",
    "import random\n",
    "column1 = sc.parallelize(range(100))\n",
    "column2 = sc.parallelize(range(100,200))\n",
    "column3 = sc.parallelize(list(reversed(range(100))))\n",
    "column4 = sc.parallelize(random.sample(range(100),100))\n",
    "data = column1.zip(column2).zip(column3).zip(column4).map(lambda a_b_c_d : (a_b_c_d[0][0][0],a_b_c_d[0][0][1],a_b_c_d[0][1],a_b_c_d[1]) ).map(lambda a_b_c_d : [a_b_c_d[0],a_b_c_d[1],a_b_c_d[2],a_b_c_d[3]])\n",
    "print(Statistics.corr(data))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "collapsed": true
   },
   "source": [
    "Congratulations, you are done with Exercice 2"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3.5 with Spark",
   "language": "python3",
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
   "version": "3.5.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
