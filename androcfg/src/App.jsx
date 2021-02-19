import React, { useRef, useState } from "react";
import "./App.css";
import { ForceGraph3D } from "react-force-graph";

import APIService from "./lib/routing/APIService";

const R2CG_APP_HOST = "127.0.0.1"
const R2CG_APP_PORT = 5000

function App() {
	const URL = R2CG_APP_HOST + "/" + R2CG_APP_PORT;

	const [data, setData] = useState({});
	const [isLoading, setIsLoading] = useState(true);

	// function genRandomTree(N = 300, reverse = false) {
	// 	return {
	// 		nodes: [...Array(N).keys()].map((i) => ({ id: i })),
	// 		links: [...Array(N).keys()]
	// 			.filter((id) => id)
	// 			.map((id) => ({
	// 				[reverse ? "target" : "source"]: id,
	// 				[reverse ? "source" : "target"]: Math.round(Math.random() * (id - 1)),
	// 			})),
	// 	};
	// }

	const fgRef = useRef();

	async function fetchCG() {
		const response = await APIService.POSTRequest("cg");
		setData(response['m_g']);
		setIsLoading(false);
		return response
	}

	if (isLoading) {
		fetchCG();
    	return <div>Loading your apks...</div>
  	}
	else {
		return (
			<div className="App">
				<ForceGraph3D
					ref={fgRef}
					graphData={data}
					linkDirectionalParticleColor={() => "red"}
					linkDirectionalParticleWidth={6}
					linkHoverPrecision={10}
					onLinkClick={(link) => fgRef.current.emitParticle(link)}
				/>
			</div>
		)
	}
}

export default App;
