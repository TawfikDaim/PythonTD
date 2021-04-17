token = "eyJhbGciOiJ.....";
context = "someuniqueId"; 
streamingUri = "streaming.saxobank.com/sim/openapi/streaming/connection";
loggingEnabled = true;
 
_connection = $.connection(streamingUri, "authorization="+token+"&context="+context, loggingEnabled);