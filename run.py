# -*- python -*-
# author: krozin@gmail.com
# sqltest: created 2016/02/08.
# copyright

import datetime
import logging
import itertools
import functools
import multiprocessing
import os
import sqlite3
import sys
import time
import unittest
from multiprocessing import Pool

import pylib


#@benchmark
def readDB(i=0, sleep=0):
  filepathname="/tmp/test.db"
  pid=os.getpid()
  i=i+1
  if os.path.exists(filepathname):
      ttime = str(datetime.datetime.now().isoformat()[11:19])
      tdate = str(datetime.datetime.today().isoformat())
      print ("readDB: PID={}; ID={}; date={}; time={}".format(pid,i,tdate,ttime))
      conn = sqlite3.connect(filepathname)
      cursor = conn.cursor()
      cursor.execute('select COUNT(*) from sqlite3_test')
      count = cursor.fetchone()
      conn.close()
      if sleep:
          time.sleep(sleep)
      return True
  return False

#@benchmark
def writeDB(i=0, sleep=0):
  pid=os.getpid()
  filepathname="/tmp/test.db"
  i=i+1
  if os.path.exists(filepathname):
      ttime = str(datetime.datetime.now().isoformat()[11:19])
      tdate = str(datetime.datetime.today().isoformat())
      print ("writeDB: PID={}; ID={}; date={}; time={}".format(pid,i,tdate,ttime))
      logging.debug("PID={}; ID={}".format(pid,i))
      try:
          conn = sqlite3.connect(filepathname)
          cursor = conn.cursor()
          cursor.execute("UPDATE sqlite3_test SET date='{}', time='{}', uuid='{}', pid='{}' WHERE id={}".format(
              tdate,ttime, pylib.get_random_uuid(),pid, i))
          conn.commit()
          conn.close()
          if sleep:
              time.sleep(sleep)
          return True
      except:
          return False
  return False

class TestSqlite3(unittest.TestCase):
  """ Let's do something. I'm not sure that someone read comments attentively """

  def _createDB(self,x=multiprocessing.cpu_count()*10):
      self.filepathname = "test.db"
      ttime = str(datetime.datetime.now().isoformat()[11:19])
      tdate = str(datetime.datetime.today().isoformat())
      tnetworks = ["{}".format(pylib.get_random_ip4()) for i in range(0,x)]
      logging.debug(ttime,tdate, tnetworks)
      print (self.__str__()) #,ttime,tdate, tnetworks)
      if not os.path.exists(self.filepathname):
          open(self.filepathname,'w').close()
          conn = sqlite3.connect(self.filepathname)
          cursor = conn.cursor()
          cursor.execute('''CREATE TABLE IF NOT EXISTS sqlite3_test (id int, date text, time text, network text, pid real, uuid text)''')
          for id,i in enumerate(tnetworks):
              self.insert_str = "INSERT INTO sqlite3_test " \
                                "VALUES ('{}','{}','{}','{}','{}','{}')".format(
                  (id+1),tdate,ttime,i,os.getpid(),pylib.get_random_uuid())
              #print (self.insert_str)
              with conn:
                  cursor.execute(self.insert_str)
          conn.commit()
          conn.close()

  def _printDB(self):
      if os.path.exists(self.filepathname):
          conn = sqlite3.connect(self.filepathname)
          cursor = conn.cursor()
          for row in cursor.execute('select * from sqlite3_test'):
              print(row)
          conn.close()

  def _readDB(self):
      if os.path.exists(self.filepathname):
          conn = sqlite3.connect(self.filepathname)
          cursor = conn.cursor()
          cursor.execute('select COUNT(*) from sqlite3_test')
          conn.close()
          return True
      return False

  def _writeDB(self, pid=os.getpid(), id=1):
      if os.path.exists(self.filepathname):
          ttime = str(datetime.datetime.now().isoformat()[11:19])
          tdate = str(datetime.datetime.today().isoformat())
          print ("PID={}; ID={}; date={}; time={}".format(pid,id,tdate,ttime))
          logging.debug("PID={}; ID={}".format(pid,id))
          try:
              conn = sqlite3.connect(self.filepathname)
              cursor = conn.cursor()
              cursor.execute("UPDATE sqlite3_test SET date='{}', time='{}', uuid='{}', pid='{}' WHERE id={}".format(
                  tdate,ttime, pylib.get_random_uuid(),pid, id))
              conn.commit()
              conn.close()
              return True
          except:
              return False
      return False

  def _createPoolReaders(self, x=multiprocessing.cpu_count()*10, sleep=0):
      try:
          pool = Pool(multiprocessing.cpu_count()*4)
          if sleep:
              pool.map(functools.partial(readDB, sleep=sleep), range(x))
              print "OK"
          else:
              pool.map(readDB, range(x))
          return True
      except:
          print ("Exception happened but my head has survived.{}".format(sys.exc_info()))
          return False
      # TODO. I dont know what exactly I wish here.

  def _createPoolWriters(self, x=multiprocessing.cpu_count()*2, sleep=0):
      try:
          pool = Pool(multiprocessing.cpu_count()*2)
          if sleep:
              pool.map(functools.partial(writeDB, sleep=sleep), range(x))
          else:
              pool.map(writeDB, range(x*2))
          return True
      except:
          print ("Exception happened but my soul alive.{}".format(sys.exc_info()[0]))
          return False
      # TODO. White rabbit.

  def setUp(self):
      self._createDB()
      self._printDB()

  def tearDown(self):
      self._printDB()
      if os.path.exists(self.filepathname):
          os.remove(self.filepathname)
      pass

  #@unittest.skip("\ntest_readDB testing skipping\n")
  def test_readDB(self):
      self.assertTrue(self._readDB())

  #@unittest.skip("\ntest_stuped_write testing skipping\n")
  def test_stuped_write(self):
      import os
      ttime = str(datetime.datetime.now().isoformat()[11:19])
      tdate = str(datetime.datetime.today().isoformat())
      pid = os.getpid() #.getppid() - unix
      id=1
      conn = sqlite3.connect(self.filepathname)
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM sqlite3_test WHERE id=1")
      row1 = cursor.fetchone()[5]
      conn.close()

      conn = sqlite3.connect(self.filepathname)
      cursor = conn.cursor()
      cursor.execute("UPDATE sqlite3_test SET uuid='{}', pid={} WHERE id={}".format(pylib.get_random_uuid(),pid, id))
      conn.commit()
      conn.close()

      conn = sqlite3.connect(self.filepathname)
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM sqlite3_test WHERE id=1")
      row2 = cursor.fetchone()[5]
      conn.close()
      print(row1, row2, row1==row2)
      self.assertIsNot(row1,row2)


  def test_writeDB(self):
      #self._printDB()
      self.assertTrue(self._writeDB(id=1))
      #self._printDB()

  #@unittest.skip("\ntest_readDBBulk testing skipping\n")
  def test_readDBBulk(self):
      self.assertTrue(self._createPoolReaders())

  #@unittest.skip("\ntest_writeDBBulk testing skipping\n")
  def test_writeDBBulk(self):
      #self._printDB()
      self.assertTrue(self._createPoolWriters())
      #self._printDB()

  #@unittest.skip("\n test_readDBBulkSleep testing skipping\n")
  def test_readDBBulkSleep(self):
      self.assertTrue(self._createPoolReaders(sleep=1))

  #@unittest.skip("\n test_writeDBBulkSleep testing skipping\n")
  def test_writeDBBulkSleep(self):
      self.assertTrue(self._createPoolWriters(sleep=1))

if __name__ == '__main__':
    unittest.main()
