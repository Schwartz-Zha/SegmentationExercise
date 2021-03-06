from Dataset import PennFudanDataset
from Model import get_instance_segmentation_model
import torch
import utils
from engine import train_one_epoch, evaluate
from Helper import get_transform
from PIL import Image

# use our dataset and defined transformations
dataset = PennFudanDataset('/home/billy/Downloads/Dataset/PennFudanPed', get_transform(train=True))
dataset_test = PennFudanDataset('/home/billy/Downloads/Dataset/PennFudanPed', get_transform(train=False))

# split the dataset in train and test set
torch.manual_seed(1)
indices = torch.randperm(len(dataset)).tolist()
dataset = torch.utils.data.Subset(dataset, indices[:-50])
dataset_test = torch.utils.data.Subset(dataset_test, indices[-50:])

# define training and validation data loaders
data_loader = torch.utils.data.DataLoader(
    dataset, batch_size=2, shuffle=True, num_workers=4,
    collate_fn=utils.collate_fn)

data_loader_test = torch.utils.data.DataLoader(
    dataset_test, batch_size=1, shuffle=False, num_workers=4,
    collate_fn=utils.collate_fn)


#device = torch.device('cuda:1')

# our dataset has two classes only - background and person
num_classes = 2

# get the model using our helper function
model = get_instance_segmentation_model(num_classes)
## move model to the right device
#model.to(device)

# construct an optimizer
#params = [p for p in model.parameters() if p.requires_grad]
#optimizer = torch.optim.SGD(params, lr=0.005,
#                            momentum=0.9, weight_decay=0.0005)

#num_epochs = 10

#for epoch in range(num_epochs):
#    # train for one epoch, printing every 10 iterations
#    train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=10)
#    # update the learning rate
#    lr_scheduler.step()
#    # evaluate on the test dataset
#    evaluate(model, data_loader_test, device=device)


#torch.save(model.state_dict(), 'ckpt/10_epoch_model.pt')

model.load_state_dict(torch.load('ckpt/10_epoch_model.pt'))

# # pick one image from the test set
img, _ = dataset_test[0]
# # put the model in evaluation mode
model.eval()
with torch.no_grad():
    prediction = model([img])
img1 = Image.fromarray(img.mul(255).permute(1, 2, 0).byte().numpy())
img2 = Image.fromarray(prediction[0]['masks'][0, 0].mul(255).byte().cpu().numpy())
img1.show()
#img2.show()

