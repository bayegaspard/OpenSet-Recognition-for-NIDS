opt_func = torch.optim.Adam
phase = -1
startphase = 0
e = 0

parameters = {"batch_size":[100, "Number of items per batch"],"num_workers":[6, "Number of threads working on building batches"],"attemptLoad":[0, "0: do not use saves\n1:use saves"],
    "testlength":[1/4, "[0,1) percentage of training to test with"],"num_epochs":[1,"Number of times it trains on the whole trainset"],"learningRate":[0.01, "a modifier for training"],
    "threshold":[0.25,"When to declare something to be unknown"], "optimizer":"Adam", "Unknowns":"refer to unknowns.CSV","CLASSES":[15,"Number of classes, do not change"], 
    "Temperature":[1,"Energy OOD scaling parameter"]}