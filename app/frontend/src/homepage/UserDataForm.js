import React, {useState} from "react";
import Select from "react-select";

export function UserForm({data, countryList, citiesList, onSubmit}) {
    const [formData, setFormData] = useState(data);
    const [alert, setAlert] = useState('');

    function validateForm(formData) {
        if (formData.nationality.length === 0) {
            setAlert('Please select your nationalities');
            return false;
        }
        if (!formData.city) {
            setAlert('Please select your city')
            return false;
        }
        return true;
    }

    return (
        <form action="#" className="bg-white rounded pb_form_v1" onSubmit={e => {
            e.preventDefault();
            if (validateForm(formData)) onSubmit(formData);
        }}>
            <h2 className="mb-4 mt-0 text-center">Free Quote</h2>
            <div className="form-group">
                <input key="form_name" type="text" className="form-control pb_height-50 reverse" required={true}
                       placeholder="Full name"
                       value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})}/>
            </div>
            <div className="form-group">
                <input key="form_email" type="email" className="form-control pb_height-50 reverse" required={true}
                       placeholder="Email"
                       value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})}
                />
            </div>
            <div className="form-group">
                <input key="form_phone" type="text" className="form-control pb_height-50 reverse"
                       placeholder="Phone (optional)"
                       value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})}
                />
            </div>
            <div className="form-group">
                <div className="pb_select-wrap">
                    <Select
                        placeholder="Nationality"
                        options={countryList}
                        value={formData.nationality}
                        onChange={selectedOptions => setFormData({...formData, nationality: selectedOptions})}
                        isMulti
                    />
                </div>
            </div>
            <div className="form-group">
                <div className="pb_select-wrap">
                    <Select
                        placeholder="City"
                        options={citiesList}
                        value={formData.city}
                        onChange={selectedOptions => setFormData({...formData, city: selectedOptions})}
                    />
                </div>
            </div>
            {alert ? <div className="alert alert-danger">{alert}</div> : ''}
            <div className="form-group">
                <input type="submit" className="btn btn-primary btn-lg btn-block pb_btn-pill  btn-shadow-blue"
                       value="Next to step 2/3"/>
            </div>
        </form>
    )
}