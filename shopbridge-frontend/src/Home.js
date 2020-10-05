import React, { Component } from "react";
import axios from "./axios.config";
import {
  Button,
  Table,
  Modal,
  Form,
  ModalHeader,
  ModalBody,
  ModalFooter,
  FormGroup,
  Input,
  Label,
} from "reactstrap";

class Home extends Component {
  state = {
    items: [],
    newItemData: {
      name: "",
      description: "",
      price: ""
    },
    newItemModal: false
  };

  // To refresh Items when components are loaded
  componentDidMount() {
    this._refreshItems();
  }

  //Toggle the model according to state
  toggleNewItemModel() {
    this.setState({
      newItemModal: !this.state.newItemModal,
    });
  }

  //add new item to the list and call backend api
  addItem=(e)=>{
    e.preventDefault()
    
    const formData = new FormData(e.target);
    //API to call Backend to post new Item
    axios.post('/item', formData).then((response) => {
      let { items } = this.state;

      let temp_data = {
        id: response.data.id,
        name: formData.get("name"),
        description: formData.get("description"),
        price: formData.get("price")
      }
      //Updating the list withour reload.
      items.push(temp_data);

      //Initializing the state to empty after creating new item
      this.setState({items, newItemModal:false, newItemData: {
        name: "",
        description: "",
        price: ""
      }});
      
    });
  }

  //To redirect to Item detail page upon clicking the row
  handleClick(id){
    this.props.history.push('/item/'+id);
    // window.location = '/item/'+id;
  }

  //To refresh the item list from backend
  _refreshItems(){
    axios.get("/list").then((response) => {
      console.log(response.data);
      this.setState({
        items: response.data,
      });
    });
  }

  //Delete item
  deleteItem(id){
    axios.delete('/item/' + id).then((response) =>{
      this._refreshItems();
    });
  }

  render() {
    let items = this.state.items.map((item) => {
      //Belo is each row of the list
      return (
          <tr key={item.id}>
            <td style={{ cursor: "pointer" }} onClick={this.handleClick.bind(this, item.id)}><img src={process.env.REACT_APP_BACKEND_URL+'/img/'+item.id+'.jpg'} alt="icon" height="25"></img></td>
            <td style={{ cursor: "pointer" }} onClick={this.handleClick.bind(this, item.id)}>{item.name}</td>
            <td style={{ cursor: "pointer" }} onClick={this.handleClick.bind(this, item.id)}>{item.price}</td>
            <td>
              <Button color="danger" size="sm" onClick={this.deleteItem.bind(this, item.id)}>
                Delete
              </Button>
            </td>
          </tr>
      );
    });
    return (
      <div className="App container">
        <h1>ShopBridge</h1>
        <Button className="my-3" color="primary" onClick={this.toggleNewItemModel.bind(this)}>
          Add Item
        </Button>

        {/* Modal to add new Item */}
        <Modal
          isOpen={this.state.newItemModal}
          toggle={this.toggleNewItemModel.bind(this)}>
          <Form onSubmit={this.addItem}>
          <ModalHeader toggle={this.toggleNewItemModel.bind(this)}>
            Add a New Item
          </ModalHeader>
          <ModalBody>
            
            <FormGroup>
              <Label for="name">Name</Label>
              <Input
                id="name"
                name="name"
                required></Input>
            </FormGroup>
            <FormGroup>
              <Label for="description">Description</Label>
              <Input
                type="textarea"
                id="description"
                name="description"
                required></Input>
            </FormGroup>
            <FormGroup>
              <Label for="price">Price</Label>
              <Input
                id="price"
                name="price"
                type="number"
                required></Input>
            </FormGroup>
            <FormGroup>
              <Label for="imgFile">Image</Label>
              <Input type="file" name="imgFile" id="imgFile" 
                accept="image/jpeg,image/jpg"
                required/>
            </FormGroup>
            
          </ModalBody>
          <ModalFooter>
            <Button
              color="primary"
              type="submit"
            >
              Add Item
            </Button>{" "}
            <Button
              color="secondary"
              onClick={this.toggleNewItemModel.bind(this)}
            >
              Cancel
            </Button>
          </ModalFooter>
          </Form>
        </Modal>

        {/* Table Head */}
        <Table>
          <thead>
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Price</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>{items}</tbody>
        </Table>
      </div>
    );
  }
}

export default Home;
