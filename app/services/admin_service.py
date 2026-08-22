from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.user_service import security_user_data

def get_all_user_service(db: Session):
	return [
		security_user_data(user)
		for user in db.query(User).order_by(User.id).all()
	]

def get_user_by_id_service(user_id: int, db: Session):
	user = db.query(User).filter(User.id == user_id).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)
	return security_user_data(user)

def list_users_service(db: Session, search: Optional[str] = None):
	query = db.query(User)
	if search and search.strip():
		search_pattern = f"%{search.strip()}%"
		query = query.filter(
			or_(
				User.email.ilike(search_pattern),
				User.full_name.ilike(search_pattern),
			)
		)

	return [security_user_data(user) for user in query.order_by(User.id).all()]