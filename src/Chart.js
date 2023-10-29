import React from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import data from './output/output.json'

const totalcar = parseInt(data.total_cars);

const sedan = parseInt(data.count_sedan);
const uni = parseInt(data.count_universal);
const mini = parseInt(data.count_minivan);
const suv = parseInt(data.count_SUV);
const hatchback = parseInt(data.count_hatchback);

const totalmodels = sedan+uni+mini+suv+hatchback;

const num_sedan = parseInt(sedan/totalmodels*100);
const num_uni = parseInt(uni/totalmodels*100);
const num_mini = parseInt(mini/totalmodels*100);
const num_suv = parseInt(suv/totalmodels*100);
const num_hatchback = parseInt(hatchback/totalmodels*100);


console.log("================================");
console.log(totalcar, sedan, uni, mini, suv, hatchback, totalmodels);
console.log("================================");
console.log(num_hatchback,num_uni, num_sedan, num_mini, num_suv);

class PieRechartComponent extends React.Component {
   COLORS = ["#800200", "#805a00", "#248000", "#4287f5", "#600080"];
   pieData = [
      {
         name: "SEDAN",
         value: num_sedan
      },
      {
         name: "MINIVAN",
         value: num_mini
      },
      {
         name: "SUV",
         value: num_suv
      },
      {
         name: "HATCHBACK",
         value: num_hatchback
      },
      {
         name: "UNIVERSAL",
         value: num_uni
      }
   ];

   CustomTooltip = ({ active, payload, label }) => {
      if (active) {
         return (
         <div
            className="custom-tooltip"
            style={{
               backgroundColor: "#ffff",
               padding: "5px",
               border: "1px solid #cccc"
            }}
         >
            <label>{`${payload[0].name} : ${payload[0].value + "%"}`}</label>
         </div>
      );
   }
   return null;
};
render() {



   return (
      <PieChart width={730} height={300}>
      <Pie
         data={this.pieData}
         color="#000000"
         dataKey="value"
         nameKey="name"
         cx="50%"
         cy="50%"
         outerRadius={120}
         fill="#8884d8"
      >
         {this.pieData.map((entry, index) => (
            <Cell
               key={`cell-${index}`}
               fill={this.COLORS[index % this.COLORS.length]}
            />
         ))}
      </Pie>
      <Tooltip content={<this.CustomTooltip />} />
      <Legend />
      </PieChart>
      );
   }
}
export default PieRechartComponent;