import time
start_time = time.time()

if __name__ == "__main__":
    #---------------------------------------------Imports------------------------------------------
    import numpy as np
    import torch
    import torch.utils.data
    import torch.nn as nn
    import torch.optim as optim
    import os
    import glob

    #three lines from https://xxx-cook-book.gitbooks.io/python-cook-book/content/Import/import-from-parent-folder.html
    import sys
    root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(root_folder)

    #this seems really messy
    from HelperFunctions.LoadPackets import NetworkDataset
    from HelperFunctions.Evaluation import correctValCounter
    from HelperFunctions.ModelLoader import Network
    import CodeFromImplementations.OpenMaxByMaXu as OpenMaxByMaXu

    #pick a device
    device = torch.device("cpu")
    if torch.cuda.is_available():
        device = torch.device("cuda:0")


    #------------------------------------------------------------------------------------------------------

    #---------------------------------------------Hyperparameters------------------------------------------
    torch.manual_seed(0)
    BATCH = 5000
    CUTOFF = 0.1
    AUTOCUTOFF = True
    epochs = 1
    checkpoint = "/checkpoint.pth"
    #------------------------------------------------------------------------------------------------------

    #---------------------------------------------Model/data set up----------------------------------------

    NAME = "src/"+os.path.basename(os.path.dirname(__file__))

    #I looked up how to make a dataset, more information in the LoadImages file
    #images are from: http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/

    path_to_dataset = "datasets" #put the absolute path to your dataset , type "pwd" within your dataset folder from your teminal to know this path.

    def getListOfCSV(path):
        return glob.glob(path+"/*.csv")
        
    data_total = NetworkDataset(getListOfCSV(path_to_dataset),ignore=[1,3,11,14])
    unknown_data = NetworkDataset(getListOfCSV(path_to_dataset),ignore=[0,2,3,4,5,6,7,8,9,10,12,13])

    CLASSES = len(data_total.classes)

    data_train, data_test = torch.utils.data.random_split(data_total, [len(data_total)-1000,1000])
    testing = torch.utils.data.DataLoader(dataset=data_test, batch_size=BATCH, shuffle=False)
    training =  torch.utils.data.DataLoader(dataset=data_train, batch_size=BATCH, shuffle=True, num_workers=1)

    #this needs to be improved 
    data_total.isOneHot = False
    data_train2, _ = torch.utils.data.random_split(data_total, [len(data_total)-1000,1000])
    training2 = torch.utils.data.DataLoader(dataset=data_train2, batch_size=BATCH, shuffle=True)

    #load the unknown data
    unknowns = torch.utils.data.DataLoader(dataset=unknown_data, batch_size=BATCH, shuffle=False)


    model = Network(CLASSES).to(device)
    #initialize the counters, op for open because open is a keyword
    soft = correctValCounter(CLASSES, cutoff=CUTOFF)
    op = correctValCounter(CLASSES, cutoff=CUTOFF)

    if os.path.exists(NAME+checkpoint):
        model.load_state_dict(torch.load(NAME+checkpoint,map_location=device))

    criterion = nn.CrossEntropyLoss(weight=torch.tensor([1.0685e-01, 1.2354e+02, 1.8971e+00, 3.0598e+01, 4.1188e+01, 4.1906e+01,
        4.4169e+01, 1.0511e+00, 2.3597e+01, 1.6117e+02, 3.7252e+02])[:CLASSES]).to(device)
    optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.5)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.1)

    #for timing
    epoch_avrg = 0

    #------------------------------------------------------------------------------------------------------

    #---------------------------------------------Training-------------------------------------------------

    for e in range(epochs+1):
        lost_amount = 0
        epoch_start = time.time()
        for batch, (X, y) in enumerate(training):
            X = X.to(device)
            y = y.to(device)

            _, output = model(X)
            lost_points = criterion(output, y)
            optimizer.zero_grad()
            lost_points.backward()


            optimizer.step()

            lost_amount += lost_points.item()

        epoch_time = time.time() - epoch_start
        epoch_avrg = (epoch_avrg*e + time.time())/(e+1)
        print(f"Epoch took: {epoch_time} seconds")

#       --------------------------------------------------------------------------------

        #--------------------------------------Autocutoff--------------------------------
        model.eval()

        #make a call about where the cutoff is
        if AUTOCUTOFF:
            op.setWeibull(weibullmodel)
            for batch, (X, y) in enumerate(training):

                
                

                _, output = model(X)

                soft.cutoffStorage(output.detach(), "Soft")
                op.cutoffStorage(output.detach(), "Open")
            soft.autocutoff(0.73)
            op.autocutoff(0.67)


        #--------------------------------------------------------------------------------

        #--------------------------------------Testing-----------------------------------

        try:       
            with torch.no_grad():
                model.eval()

                unknownscore = 0
                
                #these three lines somehow setup for the openmax thing
                scores, mavs, distances = OpenMaxByMaXu.compute_train_score_and_mavs_and_dists(CLASSES,training2,device,model)
                catagories = list(range(CLASSES))
                weibullmodel = OpenMaxByMaXu.fit_weibull(mavs,distances,catagories,tailsize=10)

                op.setWeibull(weibullmodel)

                for batch,(X,y) in enumerate(testing):
                    X = X.to(device)
                    y = y.to("cpu")

                    _, output = model(X)

                    output = output.to("cpu")

                    

                    soft.evalN(output,y)
                    if e>8:
                        op.evalN(output,y, type="Open")


                
                print(f"-----------------------------Epoc: {e}-----------------------------")
                print(f"Lost in training: {100*lost_amount/len(data_train)}")
                print("SoftMax:")
                soft.PrintEval()
                if e>8:
                    print("OpenMax:")
                    op.PrintEval()

                if e%5 == 4:
                    torch.save(model.state_dict(), NAME+checkpoint)

                soft.zero()
                op.zero()

                model.train()
        except:
            print("doge")

    #------------------------------------------------------------------------------------------------------

    #---------------------------------------------Unknowns-------------------------------------------------

    with torch.no_grad():
        unknownscore = 0
        model.eval()
        #these three lines somehow setup for the openmax thing
        scores, mavs, distances = OpenMaxByMaXu.compute_train_score_and_mavs_and_dists(CLASSES,training2,device,model)
        catagories = list(range(CLASSES))
        weibullmodel = OpenMaxByMaXu.fit_weibull(mavs,distances,catagories,tailsize=10)

        op.setWeibull(weibullmodel)

        for batch,(X,y) in enumerate(unknowns):
            X = X.to(device)
            y = y.to("cpu")
            
            _, output = model(X)

            output = output.to("cpu")


            soft.evalN(output,y, offset=-CLASSES)
            op.evalN(output,y, offset=-CLASSES,type="Open")

        print("SoftMax:")
        soft.PrintUnknownEval()
        print("OpenMax:")
        op.PrintUnknownEval()

        soft.zero()
        op.zero()
        
        model.train()

    print(f"Program took: {time.time() - start_time}")