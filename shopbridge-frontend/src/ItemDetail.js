import React, { Component } from "react";
import axios from "./axios.config";
import { Button } from "reactstrap";

class ItemDetail extends Component {
  state = {
    id:"",
    name: "",
    description: "",
    price: "",
    error: false
  };
  
  //Load item details from backend
  componentDidMount() {
    console.log(this.props.match.params.id);
    this._refreshItems(this.props.match.params.id);
  }

  _refreshItems(id){
    axios.get("/item/" + id).then((response) => {
      console.log(response.data);
      this.setState({
        id: id,
        name: response.data.name,
        description: response.data.description,
        price: response.data.price,
        error: false
      });
      document.title = response.data.name + ' | Shopbridge';
    }).catch(err => {
      this.setState({
        error: true
      })
    });
  }

  //To handle back button navigation
  handleClick(){
    this.props.history.goBack();
  }

  render() {
    if(this.state.error){
      return(
        <div className="App container">
        <div class="row">
        <p>&nbsp;</p>
        </div>
        <div class="row">
        <Button color="danger" onClick={this.handleClick.bind(this)}>Back</Button>
        </div>
        <div class="row">
        <p>&nbsp;</p>
        </div>
        <div class="row">
          <p>No Item Found!</p>
        </div>    
      </div>
      )
    }
    return (
      <div className="App container">
        <div class="row">
        <p>&nbsp;</p>
        </div>
        <div class="row">
        <Button color="danger" onClick={this.handleClick.bind(this)}>Back</Button>
        </div>
        <div class="row">
        <p>&nbsp;</p>
        </div>
        <div class="row">
          <div class="col-4">
          <img src={process.env.REACT_APP_BACKEND_URL+'/img/'+this.state.id+'.jpg'} alt="full img" width="100%"></img>
          </div>
          <div class="col-8">
            <p>&nbsp;</p>
            <h1>{this.state.name}</h1>
            <br/>
            <h3 style={{color:"red"}}>Details: </h3><h4>{this.state.description}</h4>
            <p>&nbsp;</p>
            <h2 style={{color:"red"}}>₹{this.state.price}</h2>
          </div>
        </div>    
      </div>
    );
  }
}

export default ItemDetail;
