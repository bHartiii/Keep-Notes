from rest_framework import permissions

class IsCollaborator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        collaborators = []
        collaborators = obj.collaborator.all()
        if obj.owner == request.user:
            return True
        elif collaborators:    
            for collaborator in collaborators:
                if collaborator == request.user:
                    return True  
        else:
            return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        else:
            return False
 
