import React from 'react';
import API from 'common/api';
import 'customer_detail/customer_detail.scss';

export default class CustomerDetail extends React.Component {
    constructor(prop) {
        super(prop);
        this.state = {
            customer: {},
            postcards: [],
        };
    }

    componentDidMount() {
        const { match: { params } } = this.props;
        API.get(`customers/${params.id}`)
            .then(res => this.setState({
                customer: res.data,
            }))
        API.get(`postcards/?customer_id=${params.id}`)
            .then(res => this.setState({
                postcards: res.data,
            }))
    }

    getCustomerName() {
        let customer = this.state.customer;
        return `${customer.first_name} ${customer.last_name}`
    }

    getCustomerAddress() {
        let customer = this.state.customer;
        return `${customer.address1} ${customer.address2} ${customer.city} ${customer.state} ${customer.code}`
    }

    render() {
        let rows = this.state.postcards.map(postcard => (
            <tr key={postcard.id.toString()}>
                <td>{postcard.lob_id}</td>
                <td><a href={postcard.lob_url}>Postcard</a></td>
                <td>{postcard.created}</td>
                <td>{postcard.lob_expected_delivery_date}</td>
            </tr>
        ))
        let hasPostcards = this.state.postcards.length > 0;

        return (
            <div className='customer'>
                <dl className='customer__info'>
                    <dt>Customer ID</dt>
                    <dd>{this.state.customer.id}</dd>
                    <dt>Name</dt>
                    <dd>{this.getCustomerName()}</dd>
                    <dt>Address</dt>
                    <dd>{this.getCustomerAddress()}</dd>
                </dl>
                {hasPostcards ? (
                    <table className='customer__postcards'>
                        <thead>
                            <tr>
                                <th>Lob ID</th>
                                <th>Postcard URL</th>
                                <th>Created Date</th>
                                <th>Expected Delivery Date</th>
                            </tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                ) : (
                    <div>No Postcards Yet</div>
                )}
            </div>
        )
    }
}