import React from 'react';
import {
    get,
    clone,
    set,
} from 'lodash';

export default class CustomerForm extends React.Component {
    constructor(prop) {
        super(prop);
        this.state = {
            errors: {},
        }

        this.handleFirstNameChange = this.handleFirstNameChange.bind(this);
        this.handleLastNameChange = this.handleLastNameChange.bind(this);
        this.handleAddress1Change = this.handleAddress1Change.bind(this);
        this.handleAddress2Change = this.handleAddress2Change.bind(this);
        this.handleCityChange = this.handleCityChange.bind(this);
        this.handleStateChange = this.handleStateChange.bind(this);
        this.handleCodeChange = this.handleCodeChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleFirstNameChange(event) {
        this.setState({
            first_name: event.target.value,
            errors: set(clone(this.state.errors), 'first_name', [])
        })
    }

    handleLastNameChange(event) {
        this.setState({
            last_name: event.target.value,
            errors: set(clone(this.state.errors), 'last_name', [])
        })
    }

    handleAddress1Change(event) {
        this.setState({
            address1: event.target.value,
            errors: set(clone(this.state.errors), 'address1', [])
        })
    }

    handleAddress2Change(event) {
        this.setState({
            address2: event.target.value,
            errors: set(clone(this.state.errors), 'address2', [])
        })
    }

    handleCityChange(event) {
        this.setState({
            city: event.target.value,
            errors: set(clone(this.state.errors), 'city', [])
        })
    }

    handleStateChange(event) {
        this.setState({
            state: event.target.value,
            errors: set(clone(this.state.errors), 'state', [])
        })
    }

    handleCodeChange(event) {
        this.setState({
            code: event.target.value,
            errors: set(clone(this.state.errors), 'code', [])
        })
    }

    errors(field_name) {
        let errors = get(this.state, `errors.${field_name}`, []);
        return errors.map(error => <li>{error}</li>)
    }

    handleSubmit(event) {
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit} className="customerform">
                <label className="customerform__firstname">
                    First Name:
                    <input type="text" value={this.state.first_name}  onChange={this.handleFirstNameChange}></input>
                    <ul className="customerform__errors">{this.errors('first_name')}</ul>
                </label>
                <label className="customerform__lastname">
                    Last Name:
                    <input type="text" value={this.state.last_name}  onChange={this.handleLastNameChange}></input>
                    <ul className="customerform__errors">{this.errors('last_name')}</ul>
                </label>
                <label className="customerform__address1">
                    Address1:
                    <input type="text" value={this.state.address1} onChange={this.handleAddress1Change}></input>
                    <ul className="customerform__errors">{this.errors('address1')}</ul>
                </label>
                <label className="customerform__address2">
                    Address2:
                    <input type="text" value={this.state.address2} onChange={this.handleAddress2Change}></input>
                    <ul className="customerform__errors">{this.errors('address2')}</ul>
                </label>
                <label className="customerform__city">
                    City:
                    <input type="text" value={this.state.city} onChange={this.handleCityChange}></input>
                    <ul className="customerform__errors">{this.errors('city')}</ul>
                </label>
                <label className="customerform__state">
                    State:
                    <input type="text" value={this.state.state} onChange={this.handleStateChange}></input>
                    <ul className="customerform__errors">{this.errors('state')}</ul>
                </label>
                <label className="customerform__code">
                    Code:
                    <input type="text" value={this.state.code} onChange={this.handleCodeChange}></input>
                    <ul className="customerform__errors">{this.errors('code')}</ul>
                </label>
                <input type="submit" className="customerform__submit" value="Save"></input>
            </form>
        )
    }
}