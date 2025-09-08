from datetime import datetime

class ChangeTracker:
    def __init__(self):
        self.changes = []

    def compare_product_data(self, current_data, database_data):
        """
        Compare current product data with database data and track changes.
        
        Args:
            current_data: dict with keys 'quantity', 'price', 'status'
            database_data: dict with keys 'quantity', 'price', 'status'
        
        Returns:
            dict: Changes detected
        """
        changes = {}
        
        if current_data.get('quantity') != database_data.get('quantity'):
            changes['quantity'] = {
                'old': database_data.get('quantity'),
                'new': current_data.get('quantity')
            }
        
        if current_data.get('price') != database_data.get('price'):
            changes['price'] = {
                'old': database_data.get('price'),
                'new': current_data.get('price')
            }
        
        if current_data.get('status') != database_data.get('status'):
            changes['status'] = {
                'old': database_data.get('status'),
                'new': current_data.get('status')
            }
        
        return changes

    def add_change(self, product_id, product_name, changes):
        """
        Add a change record to the tracker.
        
        Args:
            product_id: str
            product_name: str
            changes: dict of changes
        """
        change_record = {
            'product_id': product_id,
            'product_name': product_name,
            'changes': changes,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.changes.append(change_record)

    def get_changes(self):
        """
        Get all tracked changes.
        
        Returns:
            list: List of change records
        """
        return self.changes

    def clear_changes(self):
        """
        Clear all tracked changes.
        """
        self.changes = []

    def format_changes_for_email(self):
        """
        Format changes for email notification.
        
        Returns:
            str: Formatted string of changes
        """
        if not self.changes:
            return "No changes detected."
        
        email_content = "Product Changes Detected:\n\n"
        
        for change in self.changes:
            email_content += f"Product: {change['product_name']} (ID: {change['product_id']})\n"
            email_content += f"Timestamp: {change['timestamp']}\n"
            
            for field, change_data in change['changes'].items():
                email_content += f"  {field.capitalize()}: {change_data['old']} -> {change_data['new']}\n"
            
            email_content += "\n"
        
        return email_content

if __name__ == "__main__":
    # Example usage
    tracker = ChangeTracker()
    
    # Example data
    current = {'quantity': 15, 'price': 12.99, 'status': 'In Stock'}
    database = {'quantity': 10, 'price': 9.99, 'status': 'In Stock'}
    
    changes = tracker.compare_product_data(current, database)
    if changes:
        tracker.add_change("PROD001", "Test Product", changes)
    
    print(tracker.format_changes_for_email())

