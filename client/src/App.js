import "./App.css";
import Navbar from "./Components/Navbar";
import Upload from "./Components/Upload";
import About from "./Components/About";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Upload />
      <div id="about">
        <About />
      </div>
    </div>
  );
}
export default App;
