from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User

def security_user_data(user: User):
	return {
		"id": user.id,
		"email": user.email,
		"full_name": user.full_name,
		"role": user.role,
		"is_active": user.is_active,
		"created_at": user.created_at,
	}

def get_user_profile_service(current_user: dict, db: Session):
	user = db.query(User).filter(User.email == current_user["email"]).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)
	return security_user_data(user)
