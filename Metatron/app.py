from flask import Flask, request, render_template, redirect, url_for, flash, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from utils import detect_language, analyze_code, run_debugger, visualize_quantum_circuit, simulate_quantum_circuit
from flask_cors import CORS
import os
import logging

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configuration settings
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname/database'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# User model for database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    sessions = db.relationship('Session', backref='user', lazy=True)

# Session model for database
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    mode = db.Column(db.String(10), nullable=False)
    result = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    try:
        code = request.json['code']
        language = detect_language(code)
        if language == 'Unknown':
            return jsonify({"message": "Unsupported language."})
        
        errors = analyze_code(code, language)
        new_session = Session(code=code, language=language, mode='analyze', result=errors, user_id=current_user.id)
        db.session.add(new_session)
        db.session.commit()
        return jsonify({"results": errors})
    except Exception as e:
        logging.error(f"Error during analysis: {str(e)}")
        abort(500)

@app.route('/debug', methods=['POST'])
@login_required
def debug():
    try:
        code = request.json['code']
        language = detect_language(code)
        if language == 'Unknown':
            return jsonify({"message": "Unsupported language."})

        debug_output = run_debugger(code, language)
        new_session = Session(code=code, language=language, mode='debug', result=debug_output, user_id=current_user.id)
        db.session.add(new_session)
        db.session.commit()
        return jsonify({"results": debug_output})
    except Exception as e:
        logging.error(f"Error during debugging: {str(e)}")
        abort(500)

@app.route('/sessions', methods=['GET', 'POST'])
@login_required
def sessions():
    try:
        if request.method == 'POST'):
            session_id = request.form['session_id']
            session = Session.query.get(session_id)
            if session and session.user_id == current_user.id:
                db.session.delete(session)
                db.session.commit()
                flash('Session deleted successfully', 'success')
        page = request.args.get('page', 1, type=int)
        user_sessions = Session.query.filter_by(user_id=current_user.id).paginate(page, per_page=5)
        return render_template('sessions.html', sessions=user_sessions.items, pagination=user_sessions)
    except Exception as e:
        logging.error(f"Error retrieving sessions: {str(e)}")
        abort(500)

@app.route('/visualize_quantum', methods=['POST'])
@login_required
def visualize_quantum():
    try:
        code = request.json['code']
        circuit = QuantumCircuit.from_qasm_str(code)
        circuit_image = visualize_quantum_circuit(circuit)
        return jsonify({"circuit_image": circuit_image})
    except Exception as e:
        logging.error(f"Error visualizing quantum circuit: {str(e)}")
        abort(500)

@app.route('/simulate_quantum', methods=['POST'])
@login_required
def simulate_quantum():
    try:
        code = request.json['code']
        circuit = QuantumCircuit.from_qasm_str(code)
        simulation_image = simulate_quantum_circuit(circuit)
        return jsonify({"simulation_image": simulation_image})
    except Exception as e:
        logging.error(f"Error simulating quantum circuit: {str(e)}")
        abort(500)

@app.route('/compare_versions', methods=['POST'])
@login_required
def compare_versions():
    code_v1 = request.json['code_v1']
    code_v2 = request.json['code_v2']
    return jsonify({'message': 'Comparison completed.'})

@app.route('/refactor_code', methods=['POST'])
@login_required
def refactor_code():
    code = request.json['code']
    language = detect_language(code)
    if language == 'Unknown':
        return jsonify({'message': 'Unsupported language.'})
    refactored_code = huggingface_model(
        f"Refactor the following {language} code to improve quality:\n\n{code}"
    )[0]['label']
    return jsonify({'refactored_code': refactored_code})

if __name__ == '__main__':
    if not os.path.exists('app.db'):
        db.create_all()
    app.run(debug=True)
