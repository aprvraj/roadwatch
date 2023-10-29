import './App.css';
import PieRechartComponent from './Chart'
import data from './output/output.json'
// import FetchData from './CalPieChart'

const hrs = parseInt(data.vid_hrs);
const mins = parseInt(data.vid_mins);
const secs = parseInt(data.vid_secs);
const car_count = parseInt(data.total_cars);
// const count_models = parseInt(data.count_sedan)+parseInt(data.count_minivan)+parseInt(data.count_hatchback)+parseInt(data.count_SUV)+parseInt(data.count_universal)


function refreshPage() {
  window.location.reload(false);
}


function App() {
  return (
    <div className="roadwatch">
        <div className='heading'>ROADWATCH</div>
        <hr/>

        <div className='stats-button'>
          <button onClick={refreshPage} className='button'>Get Latest Stats</button>
        </div>


        <div className='row'>
        <div className="vehicle-stats">
          <div className="data-heading">ROADWATCH STATS</div>
          <div className='total'>CLIP LENGTH <span className='car-count'>{hrs}hrs {mins} mins {secs}secs</span></div>          
          <div className='total'>TOTAL CARS PASSED: <span className='car-count'>{car_count}</span></div>          
          {/* <div className='total'>ROADWATCH ACCURACY: <span className='car-count'>{car_count/count_models*100}%</span></div>
          <p style={{textAlign:'left', paddingLeft:'1.7em'} }>FORMULA: (total cars counted({car_count}) ÷ sum of identified car-models({count_models}))*100</p>           */}
        </div>

        <div className="vehicle-stats count-p">

          <PieRechartComponent/>
          {/* <div className="data-heading">Vehicle Classfications</div>
            <div className='row'>
              <div className='details-1'>
                <div className='details-p'>SEDANs</div>
                <div className='count-p'  style={{ backgroundImage: "linear-gradient(yellow,lightgreen)", color: "darkred", }}>14</div>
              </div>

              <div className='details-1'>
              <div className='details-p'>UNIVERSALs</div>
              <div className='count-p'  style={{ backgroundImage: "linear-gradient(yellow,lightgreen)", color: "darkred", }}>14</div>
              </div>
            </div>

            <div className='row'>
              <div className='details-center'>
                <div className='details-p'>HATCHBACKs</div>
                <div className='count-p'  style={{ backgroundImage: "linear-gradient(yellow,lightgreen)", color: "darkred", }}>14</div>
              </div>
            </div>

            <div className='row'>
              <div className='details-1'>
                <div className='details-p'>SUVs</div>
                <div className='count-p'  style={{ backgroundImage: "linear-gradient(yellow,lightgreen)", color: "darkred", }}>14</div>
              </div>
              <div className='details-1'>
              <div className='details-p'>MINIVANs</div>
              <div className='count-p'  style={{ backgroundImage: "linear-gradient(yellow,lightgreen)", color: "darkred", }}>14</div>
              </div> 
            </div>*/}
        </div>
        </div>
      
    </div>
  );
}

export default App;
