import React from 'react';
import API from 'common/api';
import {
    Link,
    withRouter,
} from 'react-router-dom';
import 'customer_list/customer_list.scss';

class CustomerList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            customers: [{}],
        }
        this.handleDelete = this.handleDelete.bind(this);
    }

    componentDidMount() {
        API.get("customers/")
            .then(res => this.setState({
                customers: res.data,
            }))
    }

    handleDelete(customer_id, event) {
        API.delete(`customers/${customer_id}`)
            .then(res => window.location.reload())
            .catch(error => alert(error))
        event.preventDefault();
    }

    render() {
        let rows = this.state.customers.map(customer => {
            let detail_url = `/${customer.id}`
            let edit_url = `/edit/${customer.id}`
            let key = `${customer.id}`
            return (
                <tr key={key}>
                    <td><Link to={detail_url}>{customer.first_name} {customer.last_name}</Link></td>
                    <td>{customer.address1}</td>
                    <td>{customer.address2}</td>
                    <td>{customer.city}</td>
                    <td>{customer.state}</td>
                    <td>{customer.code}</td>
                    <td>
                        <div className="customerlist__actions">
                            <Link to={edit_url} className="customerlist__edit">Edit</Link>
                            <a className="customerlist__delete" onClick={this.handleDelete.bind(this, customer.id)}>Delete</a>
                        </div>
                    </td>
                </tr>
            )
        })
        let hasCustomers = this.state.customers.length > 0;
        return (
            <div className="customerlist">
                <div className="customerlist__header">
                    <h3>Customers</h3>
                    <Link className="customerlist__add" to='/create/'>Add Customer</Link>
                </div>
                {hasCustomers ? (
                    <table className='customerlist__table'>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Address1</th>
                                <th>Address2</th>
                                <th>City</th>
                                <th>State</th>
                                <th>Code</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                ) : <div>No Customers Yet</div>}
            </div>
        )
    }
}

export default withRouter(CustomerList)