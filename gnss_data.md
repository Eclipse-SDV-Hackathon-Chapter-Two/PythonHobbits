# GNSS

Receive GPS data by subscribing to the eCAL `gps_data` topic.

The data received is in JSON format and looks like the following:

```json
{
    "header": {
        "timestamp": "1731424000660623"
    },
    "timestamp": "1731424000660623",
    "timeUTC": "542301300000000",
    "fixMode": "FM_RTK",
    "latitude": 49.547821501166666,
    "longitude": 11.017322984666666,
    "heading": 0.0,
    "speed": 0.02778,
    "altitude": 315.246,
    "satellitesUsed": 12,
    "year": 2024,
    "month": 11,
    "day": 12,
    "secsAfterMidnight": 0.0,
    "posErr": 0.0,
    "hdop": 1.0,
    "vdop": 0.0,
    "pdop": 0.0,
    "msgCnt": 0
}
```