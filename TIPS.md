## Setting launch.json in VS Code

For DML setting:

```json
"env": {
    "CUDA_VISIBLE_DEVICES": "0"
},
"args": [
    "--device", "0",
    "--delete_old",
    "--batch_size", "180",
    "--test_batch_size", "180",
    "--setting", "margin_loss",
    "--margin_alpha", "1",
    "--margin_beta", "0.5",
    "--lr_trunk", "0.00003",
    "--lr_embedder", "0.0003",
    "--lr_loss", "0.01",
    // "--use_wandb",
]
```

For SSL setting:

```json
"env": {
    "CUDA_VISIBLE_DEVICES": "0,1",
},
"args": [
    "--device", "0", "1", 
    "--delete_old",
    "--batch_size", "180",
    "--test_batch_size", "180",
    "--setting", "simsiam",
    "--lr_trunk", "0.00003",
    "--lr_embedder", "0.0003",
    "--lr_collector", "0.0003",
    "--dataset", "imagenet",
    // "--use_wandb",
]
```