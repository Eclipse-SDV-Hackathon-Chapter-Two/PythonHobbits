# Object detection 

The inference results are provided in the eCAL topic `object_detection` as JSON data. The following example show how an object could look like:

```json
{
    "iso_time": "2024-11-05T14:23:07.263719",
    // Class labels for each bounding box
    "class_ids": [
        0.0 // person
    ],
    // Confidence scores for each box
    "confidences": [
        0.944169819355011 // confidence person
    ],
    // Boxes in [x1, y1, x2, y2] format
    "xyxy": [
        [
            141.6815185546875,  // x1
            182.14732360839844, // y1
            564.3827514648438,  // x2
            479.19677734375     // y2
        ]
    ]
}
```

**Note:** The original image size is 480x640 (width x height).

The following table describes the class ids with the corresponding lables:

| class_id | label          |
|----------|----------------|
| 0        | person         |
| 1        | bicycle        |
| 2        | car            |
| 3        | motorcycle     |
| 5        | bus            |
| 6        | train          |
| 7        | truck          |
| 9        | traffic light  |
| 11       | stop sign      |
| 12       | parking meter  |

**Note:** There is only pre-defined confidence filter applied. Find the best confidence threshold within your specific application and use-case.