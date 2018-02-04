# WaifuNet-distributed

Helper scripts for training my [WaifuNet](https://github.com/leyhline/WaifuNet) since the current amount of data (and my lack of better hardware) suggests that distributed training might be the most reasonable (and by far the cheapest) solution.

## Rationale

I currently have around 32 GB of compressed image data but my own PC is rather old. Fortunately there are around 20-30 student PCs at my University that mostly aren't used at night or during weekends. These are quite good with GeForce GTX 1080 graphics cards etc. but they only have 8 GB RAM each and I am not allowed to store large amounts of data in my personal folder. Fortunately, these computers can easily communicate over the university's network with each other.

**Solution: Distributed training**

I'll be using data parallelism and just split my dataset between maybe 8 or 16 machines. Synchronized training should be sufficient since all machines have the same specs (I think), therefore I need an additional parameter server. I also played around with [Distributed TensorFlow](https://www.tensorflow.org/deploy/distributed) and it seems to run without problems.

For getting the data into RAM it seems I need to use a cloud provider (again). *pCloud* was quite nice but maybe I also need to consider *MEGA*.

## Plan

1. Adjust a simple [ResNet](https://github.com/tensorflow/models/tree/master/official/resnet) model for distributed training.
2. Code some scripts for fetching data and starting worker servers.
3. ???
4. Profit.

(And on the way I have to first read some papers about distributed deep learning and some books/tutorials about some intermediate TensorFlow since I still lack some backgrounds.)

---

P.S. [Tommy Mulc's](https://github.com/tmulc18) tutorials and his paper collection on distributed learning are really useful.
