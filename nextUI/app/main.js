(function(nx){

	// instantiate NeXt app
	var app = new nx.ui.Application();

	// instantiate Topology class
	var topology = new MyTopology();
    
    // add customs icons
    topology.registerIcon("bma", "images/bma.png", 15, 15);
    topology.registerIcon("bma1", "images/bma1.png", 40, 48);
    topology.registerIcon("bma2", "images/bma2.png", 15, 15);

	// load topology data from app/data.js
	topology.data(topologyData);

	// bind the topology object to the app
	topology.attach(app);

	// app must run inside a specific container. In our case this is the one with id="topology-container"
	app.container(document.getElementById("topology-container"));

})(nx);
