import React, { Component } from 'react';

class MyComponent extends Component {
  state = {
    data: {} // Initialize data object
  };

  async FetchData() {
    try {
      const data = await import('./analysis_results_4.json');
      this.setState({ data }); // Update component state with imported data
      console.log(data);
    } catch (error) {
      console.error('Error importing data:', error);
    }
  }

  componentDidMount() {
    // Call FetchData when the component mounts
    this.FetchData();
  }

  render() {
    // Calculate totalpercent based on state data
    const {
      count_sedan,
      count_universal,
      count_minivan,
      count_SUV,
      count_hatchback
    } = this.state.data;

    const totalpercent =
      count_sedan +
      count_universal +
      count_minivan +
      count_SUV +
      count_hatchback;

    return (
      <div>
        <p>Total Percent: {totalpercent}</p>
      </div>
    );
  }
}

export default MyComponent;
