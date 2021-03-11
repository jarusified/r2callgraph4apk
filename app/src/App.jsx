import React, { useRef, useState } from "react";
import "./App.css";
import { Column, Row } from "simple-flexbox";
import { ForceGraph3D } from "react-force-graph";

import APIService from "./lib/routing/APIService";

function App() {
	const [bData, setBData] = useState({});
	const [mData, setMData] = useState({});
	const [isLoading, setIsLoading] = useState(true);

	const fgRef = useRef();

	async function fetchCG() {
		const response = await APIService.POSTRequest("cg");
		setMData(response['m_g']);
		setBData(response['b_g']);
		setIsLoading(false);
		console.log(response);
		return response
	}

	if (isLoading) {
		fetchCG();
    	return <div>Loading your apks...</div>
  	}
	else {
		return (
			<Row className="App">
				<Column className="graph-view">
					<Row justifyContent="center" style={{ fontSize: '30px' }}> Benign APK</Row>
					<ForceGraph3D
						ref={fgRef}
						graphData={bData}
						linkDirectionalParticleColor={() => "red"}
						linkDirectionalParticleWidth={6}
						linkHoverPrecision={10}
						onLinkClick={(link) => fgRef.current.emitParticle(link)}
						width={window.innerWidth/2}
						nodeColor="blue"

					/>
				</Column>
				<Column className="graph-view">
					<Row justifyContent="center" style={{ fontSize: '30px' }}> Malicious APK</Row>
					<ForceGraph3D
						ref={fgRef}
						graphData={mData}
						linkDirectionalParticleColor={() => "red"}
						linkDirectionalParticleWidth={6}
						linkHoverPrecision={10}
						onLinkClick={(link) => fgRef.current.emitParticle(link)}
						width={window.innerWidth/2}
					/>
				</Column>
			</Row>
		)
	}
}

export default App;
