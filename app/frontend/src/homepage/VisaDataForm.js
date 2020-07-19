import React, {useState} from "react";

export function VisaForm({data, onSubmit, onBack}) {
    const [formData, setFormData] = useState(data);
    return (
        <form action="#" className="bg-white rounded pb_form_v1" onSubmit={e => {
            e.preventDefault();
            onSubmit(formData);
        }}>
            <h2 className="mb-4 mt-0 text-center">Free Quote</h2>
            <h3 className="mb-4 mt-0 text-center">Step 3/3</h3>
            <div className="form-group">
                <label htmlFor="type">Visa type</label>
                <input required={true} id="type" key="form_visa_type" type="text"
                       className="form-control pb_height-50 reverse"
                       placeholder="Current visa type"
                       value={formData.type} onChange={e => setFormData({...formData, type: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="issue_place">Issue Place</label>
                <input required={true} id="issue_place" key="issue_place" type="text"
                       className="form-control pb_height-50 reverse"
                       placeholder="Where did the visa was issued"
                       value={formData.issue_place}
                       onChange={e => setFormData({...formData, issue_place: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="issue_place">Issue Date</label>
                <input required={true} id="issue_date" key="issue_date" type="date"
                       className="form-control pb_height-50 reverse"
                       placeholder="When did the visa was issued"
                       value={formData.issue_date}
                       onChange={e => setFormData({...formData, issue_date: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="issue_place">Visa Expiration Date</label>
                <input id="expiration" key="expiration" type="date" className="form-control pb_height-50 reverse"
                       placeholder="When will the visa expire"
                       value={formData.expiration}
                       onChange={e => setFormData({...formData, expiration: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="entry_port">Entry Port</label>
                <input required={true} id="entry_port" key="entry_port" type="text"
                       className="form-control pb_height-50 reverse"
                       placeholder="Where you entered Vietnam"
                       value={formData.entry_port}
                       onChange={e => setFormData({...formData, entry_port: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="issue_place">Entry Date</label>
                <input required={true} id="entry_date" key="entry_date" type="date"
                       className="form-control pb_height-50 reverse"
                       placeholder="When you entered Vietnam"
                       value={formData.entry_date}
                       onChange={e => setFormData({...formData, entry_date: e.target.value})}/>
            </div>
            <div className="form-group">
                <input type="submit" className="btn btn-primary btn-lg btn-block pb_btn-pill  btn-shadow-blue"
                       value="Submit"/>
            </div>
            <div className="form-footer">
                <small>
                    <a href="" onClick={e => {
                        e.preventDefault();
                        onBack(formData);
                    }}><i className="fas fa-backward"> </i> back to step 2</a>
                </small>
            </div>
        </form>
    )
}