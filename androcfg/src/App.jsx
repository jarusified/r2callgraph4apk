import React, { useRef } from "react";
import "./App.css";
import { ForceGraph3D } from "react-force-graph";

function App() {
	function genRandomTree(N = 300, reverse = false) {
		return {
			nodes: [...Array(N).keys()].map((i) => ({ id: i })),
			links: [...Array(N).keys()]
				.filter((id) => id)
				.map((id) => ({
					[reverse ? "target" : "source"]: id,
					[reverse ? "source" : "target"]: Math.round(Math.random() * (id - 1)),
				})),
		};
	}

	const data = genRandomTree();

	const fgRef = useRef();

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
	);
}

export default App;
