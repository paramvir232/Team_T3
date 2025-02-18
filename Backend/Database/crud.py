import os
from dotenv import load_dotenv
from .models import db
import dropbox
from dropbox.files import WriteMode
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import SQLAlchemyError
load_dotenv()
import cloudinary.uploader

dbx = dropbox.Dropbox(os.getenv('DROPBOX_TOKEN'))
class CRUD:
    @staticmethod
    def add_item(model, **kwargs):
        """add_item( table_name, {'id':3})"""
        try:
            item = model(**kwargs)
            db.session.add(item)
            db.session.commit()
            return {"message": "Inserted", **kwargs}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": f"Error: {str(e)}"}, 500

    @staticmethod
    def get_item(model, item_id):
        """get_item( table_name , id)"""
        try:
            item = model.query.get(item_id)
            if item is None:
                return {"message": f"Item with ID {item_id} does not exist!"}, 404
            return item.serialize() if hasattr(item, 'serialize') else item.__dict__
        except SQLAlchemyError as e:
            return {"message": f"Error: {str(e)}"}, 500
            
    @staticmethod
    def update_item(model, item_id, **kwargs):
        """update_item( table_name, id, **{'name':'prince'})"""
        try:
            item = model.query.get(item_id)
            if item is None:
                return {"message": f"Item with ID {item_id} does not exist!"}, 404
            
            for key, value in kwargs.items():
                setattr(item, key, value)
            
            db.session.commit()
            return {"message": "Updated", **kwargs}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": f"Error: {str(e)}"}, 500
            
    @staticmethod
    def delete_item(model, item_id):
        """ delete_item( table_name , id)"""
        try:
            item = model.query.get(item_id)
            if item is None:
                return {"message": f"Item with ID {item_id} does not exist!"}, 404
            
            db.session.delete(item)
            db.session.commit()
            return {"message": f"Deleted item with ID {item_id}"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": f"Error: {str(e)}"}, 500

    @staticmethod
    def get_all_items(model):
        """ get_all_item( table_name )"""
        try:
            items = model.query.all()
            return [item.serialize() if hasattr(item, 'serialize') else item.__dict__ for item in items]
        except SQLAlchemyError as e:
            return {"message": f"Error: {str(e)}"}, 500
    
    @staticmethod
    def universal_query(base_model, attributes=None, filters=None, joins=None):
        """attribute=[name,age] || filters=[age>10] ||joins=[table]"""
        try:
            # Start building the query from the base model
            query = db.session.query(*[getattr(base_model, attr) for attr in attributes]) if attributes else db.session.query(base_model)
            
            # Apply joins if provided
            if joins:
                for join_model in joins:
                    query = query.join(join_model)
            
            # Apply filters if provided
            if filters:
                query = query.filter(*filters)
            
            # Execute the query
            results = query.all()
            
            # Serialize results
            if attributes:
                serialized = [dict(zip(attributes, result)) for result in results]
            else:
                serialized = [item.serialize() for item in results]

            return serialized
        except SQLAlchemyError as e:
            return {"message": f"Database error: {str(e)}"}, 500
        except AttributeError as e:
            return {"message": f"Invalid attribute: {str(e)}"}, 400
    
    import cloudinary.uploader

def upload_image_to_cloudinary(image_file):
    """
    Uploads an image file to Cloudinary and returns the secure URL.
    
    Parameters:
        image_file (FileStorage): The image file object (from request.files).
    
    Returns:
        dict: On success, returns a dict with the URL. Otherwise, returns an error message.
    """
    try:
        # Upload the image file to Cloudinary. The file can be a file-like object.
        upload_result = cloudinary.uploader.upload(image_file)
        # Cloudinary returns many details; secure_url is the HTTPS URL.
        return {"secure_url": upload_result.get("secure_url")}
    except Exception as e:
        return {"error": str(e)}

        
    

 


            
        
