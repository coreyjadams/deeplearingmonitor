import numpy
from matplotlib import pyplot as plt
import glob
from scipy import optimize

# First, know the directory where the output is going:
outdir = "/home/coradam/deeplearning/nova_net/figures/"
sourcedir = "/home/coradam/deeplearning/nova_net/"

plot_prefix = "novanet_argoneut_"

n_training_events = 500000/16.
n_testing_events = 200000

#this is the prefix to the files:
fileprefix = "nova_argoneut_savestate_"

def readFiles():

  # This function finds all of the available files, reads them in, and combines their data
  # It returns the loss, accuracy, and testing Accuracy, and iterations where testing happened
  
  files = glob.glob(sourcedir+fileprefix+"*.npz")

  iterations = []  

  for f in files:
    # Strip off the front of the file, and the extension, to get the iteration:
    iterations.append(int(f.strip(sourcedir+fileprefix).rstrip('.npz')))

  # This sorts the two lists together:
  temp = zip(iterations,files)
  temp.sort()

  print temp

  loss_list = []
  acc_list = []
  testacc_list = []

  n_points = 0

  for iteration, filename in temp:
    dat = numpy.load(filename)
    loss_list.append(dat['loss'])
    acc_list.append(dat['accuracy'])
    # testacc_list.append(dat['testAccuracy'])
    n_points += len(dat['loss'])
  
  # Package the various things into one 
  loss = numpy.asarray(loss_list).flatten()
  acc = numpy.asarray(acc_list).flatten()
  test = numpy.asarray(testacc_list).flatten()
    
  # The test accuracy has to be combined into 

  # test = numpy.zeros(len(testacc_list))
  # testacc_it = numpy.zeros(len(testacc_list))
  # for i in xrange(len(testacc_list)):
  #   test[i] = numpy.mean(testacc_list[i])
  #   testacc_it[i] = temp[i][0]

  # return acc, loss, test, testacc_it
  return acc, loss, test


def plotLoss(loss):

  # Calculate the number of epochs this has been (using the length )

  # print loss
  # exit()

  n_iterations = len(loss)

  epochs = numpy.arange(0,n_iterations) / (1.0*n_training_events)
  

  fig, ax = plt.subplots(figsize=(12,8))

  # print len(epochs)
  # print len(loss)
  # print loss

  plt.plot(epochs,loss,label="Loss")
  plt.xlabel("Epochs",fontsize=25)
  plt.ylabel("Loss",fontsize=25)

  # Make the ticks bigger
  for tick in ax.xaxis.get_major_ticks():
      tick.label.set_fontsize(16)
  for tick in ax.yaxis.get_major_ticks():
      tick.label.set_fontsize(16)


  plt.title("Loss of Nova Net",fontsize=30)
  plt.legend(fontsize=25)
  plt.grid(True)

  plt.savefig(outdir + plot_prefix + "loss.png")
  plt.savefig(outdir + plot_prefix + "loss.pdf")

  plt.show()

def plotAccuracy(trainingAccuracy):

  n_iterations = len(trainingAccuracy)


  epochs = numpy.arange(0,n_iterations) / (1.0*n_training_events)


  # Fit the last 25 points from the training with a line
  


  fig, ax = plt.subplots(figsize=(12,8))

  plt.plot(epochs, trainingAccuracy,label="Test Accuracy")


  plt.xlabel("Epochs",fontsize=25)
  plt.ylabel("Accuracy",fontsize=25)


  # Make the ticks bigger
  for tick in ax.xaxis.get_major_ticks():
      tick.label.set_fontsize(16)
  for tick in ax.yaxis.get_major_ticks():
      tick.label.set_fontsize(16)

  plt.title("Accuracy of Nova Net")
  ax.set_ylim([0,1.4])
  plt.legend(fontsize=25)


  plt.grid(True)
  plt.show()


def main():

  accuracy, loss, test = readFiles()


  plotLoss(loss)
  plotAccuracy(accuracy)


if __name__ == '__main__':
  main()