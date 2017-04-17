// the URL of the WAMP Router (Crossbar.io)
//
var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

var httpUri;

if (document.location.origin == "file://") {
   httpUri = "http://127.0.0.1:8080/lp";

} else {
   httpUri = (document.location.protocol === "http:" ? "http:" : "https:") + "//" +
               document.location.host + "/lp";
}


// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
   // url: wsuri,
   transports: [
      {
         'type': 'websocket',
         'url': wsuri
      },
      {
         'type': 'longpoll',
         'url': httpUri
      }
   ],
   realm: "aquarasp"
});


// fired when connection is established and session attached
//
connection.onopen = function (session, details) {

   main(session);


};

function main (session) {
   // subscribe to temperature event

   var temp_act = function(args) {
     console.log('counter is', args[0].toLocaleString(undefined, { maximumFractionDigits: 2 }));
     document.getElementById('temp_act').textContent = args[0].toLocaleString(undefined, { maximumFractionDigits: 2 });
   }

  session.subscribe("de.yrrgarten.temp_act", temp_act);

}


// fired when connection was lost (or could not be established)
//
connection.onclose = function (reason, details) {

   console.log("Connection lost: " + reason);

}


// now actually open the connection
//
connection.open();
